from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from pyzbar.pyzbar import decode
# from PIL import Image

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

def student_list(request):
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


# Removed scanner view to temporarily disable scanner features
# def scanner(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image = Image.open(request.FILES['image'])
#         decoded_objects = decode(image)
#         results = [obj.data.decode('utf-8') for obj in decoded_objects]
#         return JsonResponse({'results': results})

#     return render(request, 'students/scanner.html')