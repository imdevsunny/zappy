from django.contrib import admin
from django.apps import apps
from django.contrib.auth import get_user_model
from .models import *
CustomUser = get_user_model()

# Check if the Group model is registered before attempting to unregister it


# Register the CustomUser model with your custom admin configuration
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email',]

admin.site.register(Location)
admin.site.register(CustomUser, CustomUserAdmin)