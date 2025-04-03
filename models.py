from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4


# Custom User model
class User(AbstractUser):
    ROLES_CHOICES = [                           #Defines a list of roles that a user can have. 
                                          #Each role is a tuple with a value and a human-readable name.
        ('admin', 'Admin'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
        ('registrar', 'Registrar'),
    ]
    email = models.EmailField(unique=True)  # Unique email for authentication
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default='student')

    REQUIRED_FIELDS = ['username']  # Username is still required
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for auth

    def __str__(self):
        return f"{self.email} ({self.role})"


# Department model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional

    def __str__(self):
        return self.name


# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# Issue model
class Issue(models.Model):
    issue_id = models.UUIDField(default=uuid4, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_code = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='issues')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')],
        default='pending'
    )
    priority = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_issues')
    affected_course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='affected_issues')
    affected_student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='affected_issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the object is new
        super().save(*args, **kwargs)
        if is_new:
            send_mail(
                'Issue Created',
                f'Your issue "{self.title}" has been created successfully.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                fail_silently=False,
            )

    def __str__(self):
        return self.title


# Registration model
class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registration for {self.user.email}"


# Activity Log model
class Activity(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('resolved', 'Resolved'),
    ]
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} by {self.user.username} on {self.timestamp}"



