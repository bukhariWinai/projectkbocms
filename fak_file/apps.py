from django.apps import AppConfig


class FakFileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fak_file'
