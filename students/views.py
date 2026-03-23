from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from pyzbar.pyzbar import decode
from PIL import Image
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Student, Attendance
from django.utils import timezone

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Student, Attendance
from django.utils.timezone import now

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.db.models import Q

def student_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        students = Student.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(barcode_id__icontains=search_query)
        ).order_by('last_name')
    else:
        students = Student.objects.all().order_by('last_name')
    return render(request, 'students/student_list.html', {'students': students})


def student_create(request):
    form = StudentForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('student_list')

    return render(request, 'students/student_form.html', {'form': form})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)

    if form.is_valid():
        form.save()
        return redirect('student_list')

    return render(request, 'students/student_form.html', {'form': form})


def barcode_input(request):
    if request.method == 'POST':
        barcode_id = request.POST.get('barcode_id')
        student = Student.objects.filter(barcode_id=barcode_id).first()
        if student:
            return render(request, 'students/barcode_result.html', {'student': student})
        else:
            return HttpResponse('Student not found', status=404)

    return render(request, 'students/barcode_input.html')


@csrf_exempt
def scanner(request):
    if request.method == 'POST':
        try:
            # Extract scanned data from the request
            body = json.loads(request.body)
            scanned_data = body.get('scanned_data')

            if scanned_data:
                # Check if the scanned data matches a student
                student = Student.objects.filter(barcode_id=scanned_data).first()

                if student:
                    # Fetch additional student details
                    student_details = {
                        'id': student.id,
                        'first_name': student.first_name,
                        'last_name': student.last_name,
                        'grade': student.grade,
                        'barcode_id': student.barcode_id,
                        'date_of_birth': student.date_of_birth,
                        'address': student.address,
                    }

                    # Return the student details as a JSON response
                    return JsonResponse({'status': 'success', 'student': student_details})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def scan_student_id(request):
    if request.method == 'POST' and request.FILES.get('barcode_image'):
        # Load the uploaded image
        image = Image.open(request.FILES['barcode_image'])

        # Decode the barcode/QR code
        decoded_objects = decode(image)
        if decoded_objects:
            barcode_data = decoded_objects[0].data.decode('utf-8')

            # Check if the barcode matches a student
            student = get_object_or_404(Student, barcode_id=barcode_data)

            # Record attendance
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=timezone.now().date()
            )

            if created:
                attendance.time_in = timezone.now()
                attendance.save()

            return JsonResponse({
                'status': 'success',
                'message': f'Attendance recorded for {student.first_name} {student.last_name}',
            })

        return JsonResponse({'status': 'error', 'message': 'Invalid barcode or QR code'})

    return render(request, 'students/scan_student_id.html')


def scan_qr_code(request):
    if request.method == 'POST' and request.FILES.get('qr_code_image'):
        # Load the uploaded image
        image = Image.open(request.FILES['qr_code_image'])

        # Decode the QR code
        decoded_objects = decode(image)
        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')

            # Check if the QR code matches a student
            student = get_object_or_404(Student, barcode_id=qr_data)

            # Record attendance
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=timezone.now().date()
            )

            if created:
                attendance.time_in = timezone.now()
            else:
                attendance.time_out = timezone.now()

            attendance.save()

            return JsonResponse({
                'status': 'success',
                'message': f'Attendance recorded for {student.first_name} {student.last_name}',
            })

        return JsonResponse({'status': 'error', 'message': 'Invalid QR code'})

    return render(request, 'students/scan_qr_code.html')

#######
from django.http import JsonResponse

def get_student(request, barcode_id):
    from .models import Student

    try:
        student = Student.objects.get(barcode_id=barcode_id)
        return JsonResponse({
            'name': f"{student.first_name} {student.last_name}",
            'status': student.status
        })
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'})
    

#######


def scanner_page(request):
    return render(request, 'students/scan.html')

from django.http import JsonResponse
from django.utils import timezone
from .models import Student, Attendance

def submit_scan(request, barcode_id):
    try:
        student = Student.objects.get(barcode_id=barcode_id)
        today = timezone.now().date()

        attendance, created = Attendance.objects.get_or_create(
            student=student,
            date=today
        )

        if not attendance.time_in:
            attendance.time_in = timezone.now()
            attendance.save()
            status = "TIME IN"
        elif not attendance.time_out:
            attendance.time_out = timezone.now()
            attendance.save()
            status = "TIME OUT"
        else:
            status = "ALREADY RECORDED"

        # ✅ Get today's attendance list
        today_attendance = Attendance.objects.filter(date=today).select_related('student')

        attendance_list = []
        for a in today_attendance:
            attendance_list.append({
                'name': f"{a.student.first_name} {a.student.last_name}",
                'status': "TIME OUT" if a.time_out else "TIME IN"
            })

        return JsonResponse({
            "name": f"{student.first_name} {student.last_name}",
            "status": status,
            "barcode": student.barcode_id,
            "photo": student.photo.url if student.photo else "",
            "attendance_list": attendance_list   # ✅ NEW
        })

    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"})




