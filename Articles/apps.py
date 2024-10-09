from django.apps import AppConfig
from django.contrib import admin


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Articles'
    verbose_name = "Articles & Gallery"

# Register the AdminConfig
