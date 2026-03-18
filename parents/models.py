from django.db import models

# Create your models here.
class Parent(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='parents')
    first_name = models.CharField(max_length=255, default='Unknown')
    middle_name = models.CharField(max_length=255, blank=True, null=True, default='')
    last_name = models.CharField(max_length=255, default='Unknown')
    #name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.name = f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()