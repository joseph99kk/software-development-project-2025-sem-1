from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.
# class user models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('registrar', 'Registrar'),
        ('admin', 'Admin'),
    )
    
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_group",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES )
    
    
class Admin(models.Model):
    name = models.CharField(max_length=30)
    

class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    issueID = models.TextField()
    issue = models.CharField(max_length=200)
    
    def __str__(self):
        return self.issue
    
class Registrar(models.Model):
    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    issueID = models.IntegerField()
    issue = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.issue
 class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'lecturer'})

    def __str__(self):
        return f"{self.code} - {self.name}"

    
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    issue = models.TextField()
    issueID = models.IntegerField()
    date = models.DateField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="students")
    
    def __str__(self):
        return self.issue

