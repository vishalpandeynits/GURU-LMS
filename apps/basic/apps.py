from django.apps import AppConfig


class BasicConfig(AppConfig):
    name = 'basic'

    def ready(self):
        import apps.basic.notificate