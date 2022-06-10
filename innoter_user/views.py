from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from innoter_user.models import User
from innoter_user.serializers import RegisterUserSerializer, \
    UpdateUserSerializer, ListUserSerializer, \
    DetailUserSerializer, MyTokenObtainPairSerializer, \
    DeleteUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_classes = {'list': ListUserSerializer,
                          'create': RegisterUserSerializer,
                          'update': UpdateUserSerializer,
                          'retrieve': DetailUserSerializer,
                          'delete': DeleteUserSerializer}

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy', 'list']:
    #         self.permission_classes = [IsAuthenticated, ]
    #     elif self.action in ['create']:
    #         self.permission_classes = [AllowAny, ]
    #     return super().get_permissions()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
