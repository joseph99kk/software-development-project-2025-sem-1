from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Unique email for authentication
    
    REQUIRED_FIELDS = ['username']  # Username is still required
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    
    def __str__(self):
        return self.email  # Return the email as the string representation

# Department model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique name for the department
    description = models.TextField(blank=True, null=True)  # Optional description of the department

    def __str__(self):
        return self.name  # Return the name as the string representation
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# Issue model
class Issue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    Issue_id = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='issues')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='issues')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_issues')
    affected_course = models.CharField(max_length=100, blank=True, null=True)
    affected_student = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if the object is being created (no primary key yet)
        if not self.pk:
            super().save(*args, **kwargs)  # Save the object to generate the primary key
        if not self.Issue_id:  # Generate Issue_id only if it doesn't already exist
            self.Issue_id = f"I-{self.pk:05d}"  # Generate a unique Issue ID
        super().save(*args, **kwargs)  # Save the object again with the Issue_id

# Registration model
class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registration for {self.user.email}"

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
        verbose_name_plural="Activities"
        ordering = ['-timestamp']
    def __str__(self):
        
            return f"{self.action} by {self.user.username} on {self.timestamp}"