from django.apps import AppConfig


class RestapiConfig(AppConfig):
    name = 'restapi'

    def ready(self):
        import restapi.signals