from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from innoter_user.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'image_s3_path', 'role', 'title', 'is_blocked')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'image_s3_path', 'role', 'title', 'is_blocked')
