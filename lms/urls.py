from django.urls import path
from . import views

urlpatterns = [
    path('api/courses/', views.course_list, name='api_course_list'),
    path('api/courses/<int:course_id>/', views.course_detail, name='api_course_detail'),
    path('api/analytics/', views.course_analytics, name='api_analytics'), 
    
    # --- URL UNTUK CELERY TASKS ---
    path('api/enroll/<int:course_id>/', views.enroll_student, name='api_enroll'),
    path('api/finish/<int:course_id>/', views.finish_course, name='api_finish'),
    path('api/report/', views.request_report, name='api_report'),
]