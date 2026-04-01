from functools import wraps
from datetime import datetime

from django.core.cache import cache
from django.http import JsonResponse

# --- DRF IMPORTS ---
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsInstructorOrReadOnly

# --- LOCAL IMPORTS ---
from .models import Course
from .serializers import CourseSerializer
from .tasks import send_enrollment_email, generate_certificate, export_course_report
from .mongo_client import activity_logs

def rate_limit(requests=60, window=60):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR')
            key = f"rate_limit_{ip}"
            
            current_requests = cache.get(key, 0)
            if current_requests >= requests:
                
                return JsonResponse({'error': 'Too Many Requests (Rate Limit Exceeded)'}, status=429)
            
            if current_requests == 0:
                cache.set(key, 1, window) 
            else:
                cache.incr(key)
                
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsInstructorOrReadOnly]) 
@rate_limit(requests=60)
def course_list(request):
    cache_key = 'course_list_cache'

    if request.method == 'GET':
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({'data': cached_data, 'source': 'REDIS_CACHE'})
        
        courses = Course.objects.all() 
        serializer = CourseSerializer(courses, many=True)
        data = serializer.data
        
        cache.set(cache_key, data, 60 * 15)
        return Response({'data': data, 'source': 'DATABASE'})


    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        

        if serializer.is_valid():
            serializer.save()

            cache.delete(cache_key) 
            
            return Response({
                "message": "Course berhasil ditambahkan!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@rate_limit(requests=60)
def course_detail(request, course_id):
    cache_key = f'course_detail_cache_{course_id}'
    cached_data = cache.get(cache_key)
    
    if cached_data and isinstance(cached_data, dict):
        data = cached_data
        source = 'REDIS_CACHE'
    else:
        try:
            c = Course.objects.select_related('instructor', 'category').get(id=course_id)

            data = {'id': c.id, 'title': c.title, 'description': c.description}
            
            cache.set(cache_key, data, 60 * 15) 
            source = "DATABASE"
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        

    activity_logs.insert_one({
        "action": "view_course", 
        "course_id": course_id,
        "course_title": data.get('title', 'Unknown Title'),
        "timestamp": datetime.utcnow(),
        "ip_address": request.META.get('REMOTE_ADDR')
    })
    
    return Response({'data': data, 'source': source})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_analytics(request):
    total_data_mentah = activity_logs.count_documents({})
    
    pipeline = [
        {"$match": {"action": "view_course"}}, 
        {"$group": {
            "_id": "$course_title", 
            "total_views": {"$sum": 1}
        }},
        {"$sort": {"total_views": -1}}
    ]
    results = list(activity_logs.aggregate(pipeline))
    
    return Response({
        "total_data_mentah_di_mongodb": total_data_mentah,
        "analytics_report": results
    })


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def enroll_student(request, course_id):   
    user_email = request.user.email if request.user.email else "student@example.com"
    send_enrollment_email.delay(user_email, f"Course {course_id}")
    return Response({"message": f"Pendaftaran Course {course_id} berhasil! Email konfirmasi dikirim ke {user_email} di latar belakang."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_course(request, course_id):
    student_id = request.user.id 
    generate_certificate.delay(student_id, course_id)
    return Response({"message": f"Selamat! Course selesai. Sertifikat PDF untuk user ID {student_id} sedang diproses."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_report(request):
    export_course_report.delay("admin@kampus.com")
    return Response({"message": "Request diterima! File CSV sedang digenerate dan akan dikirim ke email admin."})