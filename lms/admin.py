from django.contrib import admin
from .models import User, Category, Course, Lesson, Enrollment, Progress

# 1. Admin untuk Custom User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# 2. Admin untuk Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)

# 3. Inline Model untuk Lesson (Syarat Deliverable 3)
# Menggunakan TabularInline agar bisa nambah Lesson langsung di halaman Course
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1  # Menyediakan 1 baris kosong secara default

# 4. Admin untuk Course (Memasang Inline Lesson di sini)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category')
    list_filter = ('category', 'instructor')
    search_fields = ('title', 'description')
    inlines = [LessonInline]

# 5. Admin untuk Enrollment
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('student__username', 'course__title')

# 6. Admin untuk Progress
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('enrollment__student__username', 'lesson__title')