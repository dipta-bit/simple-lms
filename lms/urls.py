from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/courses/', views.course_list, name='api_course_list'),
    path('api/courses/<int:course_id>/', views.course_detail, name='api_course_detail'),
    path('api/analytics/', views.course_analytics, name='api_analytics'), 
    
    # --- URL CELERY TASKS ---
    path('api/enroll/<int:course_id>/', views.enroll_student, name='api_enroll'),
    path('api/finish/<int:course_id>/', views.finish_course, name='api_finish'),
    path('api/report/', views.request_report, name='api_report'),
    # ---URL LOGIN & JWT ---
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name ='token_refresh'),
]
