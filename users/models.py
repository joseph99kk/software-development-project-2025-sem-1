from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('registrar', 'Registrar'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    student_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    lecturer_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    registrar_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    
    def save(self, *args, **kwargs):
        if self.role == 'student':
            self.lecturer_number = None
            self.registrar_number = None
        elif self.role == 'lecturer':
            self.student_number = None
            self.registrar_number = None
        elif self.role == 'registrar':
            self.student_number = None
            self.lecturer_number = None
        super().save(*args, **kwargs)
