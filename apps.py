from django.apps import AppConfig


class UniConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UNI'

    def ready(self):
        from . import signals  # Import signals to ensure they are registered
        signals