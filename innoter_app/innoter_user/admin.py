from django.contrib import admin
from innoter_user.models import User
from django.contrib.auth.admin import UserAdmin
from innoter_user.forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'image_s3_path', 'role', 'title', 'is_blocked',]


admin.site.register(User, CustomUserAdmin)
