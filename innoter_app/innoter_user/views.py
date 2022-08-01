from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from innoter_user.models import User
from innoter_user.permissions import RoleIsAdmin, UserIsOwner
from innoter_user.role_action import RoleActionSerializer
from innoter_user.serializers import RegisterUserSerializer, \
    UpdateUserSerializer, ListUserSerializer, \
    DetailUserSerializer, MyTokenObtainPairSerializer, \
    AttachRoleUserSerializer, UploadPhotoSerializer
from rest_framework.decorators import action
from innoter_user.photo_file import prepare_photo
from dynamo.code.transmit_data import users
from producer import publish


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_classes = {'list': ListUserSerializer,
                          'create': RegisterUserSerializer,
                          'update': UpdateUserSerializer,
                          'retrieve': DetailUserSerializer
                          }

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, None)
        return serializer


class ACTIONUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def rgstr(self, request, *args, **kwargs):
        filename = prepare_photo(request)
        data = dict(request.data)
        del data['file']
        data.update(filename)
        for key in data.keys():
            data[key] = data[key][0]
        serializer = RegisterUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        publish("create_user", serializer.data['pk'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def all(self, request, *args, **kwargs):
        serializer = ListUserSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def info(self, request, *args, **kwargs):
        retrieve_user = self.get_object()
        serializer = DetailUserSerializer(retrieve_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[UserIsOwner])
    def upd(self, request, *args, **kwargs):
        update_me = self.get_object()
        serializer = UpdateUserSerializer(instance=update_me, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        publish("update_user", update_me.pk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], permission_classes=[UserIsOwner | RoleIsAdmin])
    def delete(self, request, *args, **kwargs):
        delete_user = self.get_object()
        publish("delete_user", delete_user.pk)
        self.perform_destroy(delete_user)
        return Response({'message': 'User has been deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'], permission_classes=[RoleIsAdmin])
    def attach_role(self, request, *args, **kwargs):

        attach_role_user = self.get_object()

        if 'roles' in request.data:
            role_serializer = RoleActionSerializer(data=request.data)
            if not role_serializer.is_valid():
                return Response(role_serializer.errors, status.HTTP_400_BAD_REQUEST)

            role = role_serializer.data.get('roles')

            if role == 'USER':
                attach_role_user.role = attach_role_user.Roles.USER
            elif role == 'MODERATOR':
                attach_role_user.role = attach_role_user.Roles.MODERATOR
            elif role == 'ADMIN':
                attach_role_user.role = attach_role_user.Roles.ADMIN

        user_serializer = AttachRoleUserSerializer(data=request.data, instance=attach_role_user, partial=True,
                                               context={'request', request})
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        publish("update_user", attach_role_user.pk)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[UserIsOwner])
    def upload_photo(self, request, *args, **kwargs):
        update_user = self.get_object()
        filename = prepare_photo(request)
        serializer = UploadPhotoSerializer(instance=update_user, data=filename)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        publish("update_user", update_user.pk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def create_table(self, request, *args, **kwargs):
        publish("create_table_users")
        return Response({'message': "Users dynamodb table created"},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def transmit(self, request, *args, **kwargs):
        try:
            publish("transmit_users")
            return Response({'message': "Existing users transmitted to dynamodb"},
                            status=status.HTTP_200_OK)
        except:
            return Response({'message': "Table Users doesn't exist"},
                            status=status.HTTP_200_OK)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
