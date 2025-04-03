from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from .models import User

@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created:  # create a user first to send email
        
        try:
            subject = "Welcome to the System"
            message = (
                f"Dear {instance.username},\n\n"
                f"Thank you for registering on our platform.\n\n"
                f"To get started, please log in to your account:\n"
                f"{settings.FRONTEND_URL}/login\n\n"
                f"Best regards,\nThe Team"
            )
            html_message = (
                f"<p>Dear {instance.username},</p>"
                f"<p>Thank you for registering on our platform.</p>"
                f"<p>To get started, please <a href='{settings.FRONTEND_URL}/login'>log in</a> to your account.</p>"
                f"<p>Best regards,<br>The Team</p>"
            )
            send_mail(
                subject=subject,
                message=strip_tags(html_message),  # Plain text version
                html_message=html_message,  # HTML version
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,  # Raises an error if the email fails to send
            )
        except Exception as e:
            print(f"Error sending registration email to {instance.email}: {e}")
