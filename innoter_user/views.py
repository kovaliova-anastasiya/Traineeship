from django.shortcuts import render
from rest_framework import viewsets
from innoter_user.models import User
from innoter_user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

