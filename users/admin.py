from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "is_staff", "is_superuser", "date_joined")

admin.site.register(User, UserAdmin)