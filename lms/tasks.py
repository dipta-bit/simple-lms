from celery import shared_task
import time


@shared_task
def send_enrollment_email(student_email, course_title):
    print(f"Mulai mengirim email ke {student_email}...")
    time.sleep(3) 
    print(f"✅ EMAIL TERKIRIM: Selamat datang di {course_title}!")
    return True


@shared_task
def generate_certificate(student_id, course_id):
    print(f"Mulai membuat desain PDF sertifikat untuk student {student_id}...")
    time.sleep(5) 
    print(f"✅ SERTIFIKAT SELESAI: Sertifikat course {course_id} siap diunduh!")
    return f"URL_SERTIFIKAT_{student_id}_{course_id}.pdf"

@shared_task
def update_course_statistics():
    print("Sedang menghitung ulang semua total enrollment...")
    time.sleep(2)
    print("✅ STATISTIK UPDATE: Semua data course sudah diperbarui ke versi terbaru.")
    return "Statistik diupdate"


@shared_task
def export_course_report(admin_email):
    print("Mulai mengambil data dari database untuk file CSV...")
    time.sleep(4) 
    print(f"✅ EXPORT SELESAI: File CSV berhasil dikirim ke {admin_email}")
    return "Report_Courses.csv"