"""
Admin configuration for the accounts app.
"""

# Django imports
from django.contrib import admin

# Local imports
from .models import User

# Register your models here.
admin.site.register(User)
