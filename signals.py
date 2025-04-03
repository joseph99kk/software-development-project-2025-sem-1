from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import User

@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to the System"
        recipient_email = instance.email

        # Render HTML email
        email_html_content = render_to_string("emails/welcome_email.html", {"username": instance.username})
        
        # Send email with both plain text and HTML
        email = EmailMultiAlternatives(
            subject=subject,
            body="Welcome to the system!",  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(email_html_content, "text/html")
        email.send()

        
