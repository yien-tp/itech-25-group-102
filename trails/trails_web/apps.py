from django.apps import AppConfig


class TrailsWebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trails_web"


    def ready(self):
        import trails_web.signals  # Import signals when the app is ready