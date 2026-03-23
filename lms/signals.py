# lms/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Course

@receiver([post_save, post_delete], sender=Course)
def invalidate_course_cache(sender, instance, **kwargs):
    
    cache.delete('course_list_cache')
    cache.delete(f'course_detail_cache_{instance.id}')
    print(f"[CACHE CLEARED] Cache untuk Course '{instance.title}' telah dihapus.")