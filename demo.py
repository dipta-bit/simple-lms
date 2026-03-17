import os
import django
from django.db import connection, reset_queries

# Setup Environment agar script bisa mengakses database Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lms.models import User, Category, Course

def seed_data():
    """Mengisi Data Awal (Deliverable 5: Fixtures)"""
    if Course.objects.exists():
        print("Data sudah ada, skip pembuatan fixtures...\n")
        return
    
    print("⏳ Menambahkan data dummy ke database...\n")
    cat1 = Category.objects.create(name="Backend Development")
    cat2 = Category.objects.create(name="Frontend Development")
    
    inst1 = User.objects.create(username="pak_budi", role="instructor")
    inst2 = User.objects.create(username="bu_siti", role="instructor")
    
    # Bikin 10 Course dummy
    for i in range(1, 11):
        Course.objects.create(
            title=f"Course Mantap {i}",
            description="Belajar programming dari nol",
            instructor=inst1 if i % 2 == 0 else inst2,
            category=cat1 if i % 2 == 0 else cat2
        )

def demo_unoptimized():
    print("=== ❌ UNOPTIMIZED QUERY (N+1 Problem) ===")
    reset_queries() # Reset penghitung
    
    courses = list(Course.objects.all()) # 1 Query ke tabel Course
    for course in courses:
        # Loop ini memicu query TAMBAHAN ke tabel User & Category tiap baris!
        print(f"- {course.title} | {course.instructor.username} | {course.category.name}")
    
    query_count = len(connection.queries)
    print(f"\nTotal Queries ke Database: {query_count}\n")
    return query_count

def demo_optimized():
    print("=== ✅ OPTIMIZED QUERY (Menggunakan select_related) ===")
    reset_queries() # Reset penghitung
    
    # Memanggil custom manager .for_listing() yang kita buat di Deliverable 2
    courses = list(Course.objects.for_listing()) 
    for course in courses:
        # TIDAK ADA query tambahan karena data sudah di-JOIN sejak awal
        print(f"- {course.title} | {course.instructor.username} | {course.category.name}")
    
    query_count = len(connection.queries)
    print(f"\nTotal Queries ke Database: {query_count}\n")
    return query_count

if __name__ == '__main__':
    seed_data()
    unopt_count = demo_unoptimized()
    opt_count = demo_optimized()
    
    print("========== 🏆 KESIMPULAN ==========")
    print(f"Tanpa optimasi, Django melakukan {unopt_count} queries.")
    print(f"Dengan optimasi, Django HANYA melakukan {opt_count} query!")