from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
import barcode
from barcode.writer import ImageWriter


from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
import barcode
from barcode.writer import ImageWriter
from django.utils import timezone

class Student(models.Model):
    first_name = models.CharField(max_length=255, default='Unknown')
    middle_name = models.CharField(max_length=255, blank=True, null=True, default='')
    last_name = models.CharField(max_length=255, default='Unknown')
    dob = models.DateField()
    barcode_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    
    # ✅ Added student photo
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True)

    def save(self, *args, **kwargs):
        # Generate QR Code
        qr = qrcode.make(self.barcode_id)
        qr_io = BytesIO()
        qr.save(qr_io, format='PNG')
        self.qr_code.save(f'{self.barcode_id}_qr.png', File(qr_io), save=False)

        # Generate Barcode
        CODE128 = barcode.get_barcode_class('code128')
        barcode_obj = CODE128(self.barcode_id, writer=ImageWriter())
        barcode_io = BytesIO()
        barcode_obj.write(barcode_io)
        self.barcode_image.save(f'{self.barcode_id}_barcode.png', File(barcode_io), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()


from django.utils import timezone

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    scanned_id = models.CharField(max_length=100, blank=True, null=True, help_text="Temporary field to store scanned student ID.")
    
    def __str__(self):
        return f"{self.student} - {self.date}"