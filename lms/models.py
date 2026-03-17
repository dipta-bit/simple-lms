from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

# 2. Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# 3. Custom Managers untuk Optimasi (Deliverable 2)
class CourseManager(models.Manager):
    def for_listing(self):
        # Mencegah N+1 Problem dengan mengambil relasi di awal
        return self.get_queryset().select_related('instructor', 'category')

class EnrollmentManager(models.Manager):
    def for_student_dashboard(self):
        return self.get_queryset().select_related('course').prefetch_related(
            'progress', 
            'progress__lesson'
        )

# 4. Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'}, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')

    # 👇 INI KUNCI UTAMANYA: Memasang manager ke model
    objects = CourseManager()

    def __str__(self):
        return self.title

# 5. Lesson Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(help_text="Urutan materi")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# 6. Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    objects = EnrollmentManager()

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

# 7. Progress Model
class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('enrollment', 'lesson')

    def __str__(self):
        return f"Progress {self.enrollment.student.username} - {self.lesson.title}"