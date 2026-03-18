# Register your models here.

from django.contrib import admin
from .models import Student
from django.utils.html import format_html

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'barcode_id', 'qr_preview', 'barcode_preview')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.middle_name or ''} {obj.last_name}".strip()
    full_name.short_description = 'Full Name'

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />', obj.qr_code.url)
        return ""

    def barcode_preview(self, obj):
        if obj.barcode_image:
            return format_html('<img src="{}" width="100" height="50" />', obj.barcode_image.url)
        return ""