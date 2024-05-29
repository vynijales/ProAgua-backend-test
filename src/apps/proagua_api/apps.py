from django.apps import AppConfig


class ProaguaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.proagua_api'

    def ready(self):
        import apps.proagua_api.signals
