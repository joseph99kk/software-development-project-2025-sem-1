from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created:  # Send email only when a new user is created
        send_mail(
            subject="Welcome to the System",
            message=f"Dear {instance.username},\n\n"
                    f"Thank you for registering on our platform.\n"
                    f"Please log in to your account to get started.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )