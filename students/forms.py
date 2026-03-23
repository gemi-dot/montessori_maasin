from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'dob',
            'barcode_id',
            'status',
            'status',
            'photo'
        ]

    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        'barcode_id': forms.TextInput(attrs={'class': 'form-control'}),
        'status': forms.TextInput(attrs={'class': 'form-control'}),
        'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
}




