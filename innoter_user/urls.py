from rest_framework import routers
from innoter_user.views import UserViewSet


user_router = routers.SimpleRouter()
user_router.register(r'users', UserViewSet)
