from django.apps import AppConfig


class VendConfig(AppConfig):
    name = 'vend'


class LoadReceivers(AppConfig):
    name = 'vend'

    def ready(self):
        from . import receivers