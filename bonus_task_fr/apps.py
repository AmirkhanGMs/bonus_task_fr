# apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app_name'  # Укажите здесь название вашего приложения

    def ready(self):
        # Импорт здесь, чтобы избежать проблем циклических импортов
        from . import signals
