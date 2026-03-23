# lms/views.py
from .tasks import send_enrollment_email, generate_certificate, export_course_report
from django.core.cache import cache
from django.http import JsonResponse
from .models import Course
from functools import wraps
from datetime import datetime
from .mongo_client import activity_logs

# Rate Limiting Decorator (60 requests/minute)
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


@rate_limit(requests=60)
def course_list(request):
    cache_key = 'course_list_cache'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return JsonResponse({'data': cached_data, 'source': 'REDIS_CACHE'})
    
    courses = Course.objects.for_listing()
    data = [{'id': c.id, 'title': c.title, 'instructor': c.instructor.username} for c in courses]
    
    cache.set(cache_key, data, 60 * 15)
    
    return JsonResponse({'data': data, 'source': 'DATABASE'})

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
            return JsonResponse({'error': 'Course not found'}, status=404)
        
    activity_logs.insert_one({
        "action": "view_course", 
        "course_id": course_id,
        "course_title": data.get('title', 'Unknown Title'),
        "timestamp": datetime.utcnow(),
        "ip_address":request.META.get('REMOTE_ADDR')
    })
    
    return JsonResponse({'data': data, 'source': source})


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
    
    return JsonResponse({
        "total_data_mentah_di_mongodb": total_data_mentah,
        "analytics_report": results
    })


def enroll_student(request, course_id):   
    send_enrollment_email.delay("student@example.com", f"Course {course_id}")
    

    return JsonResponse({"message": f"Pendaftaran Course {course_id} berhasil! Email konfirmasi sedang dikirim di latar belakang."})

def finish_course(request, course_id):
    dummy_student_id = 99
    generate_certificate.delay(dummy_student_id, course_id)
    return JsonResponse({"message": "Selamat! Course selesai. Sertifikat PDF Anda sedang diproses dan akan segera siap."})

def request_report(request):
    export_course_report.delay("admin@kampus.com")
    return JsonResponse({"message": "Request diterima! File CSV sedang digenerate dan akan dikirim ke email admin."})
