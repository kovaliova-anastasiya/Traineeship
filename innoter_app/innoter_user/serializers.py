from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from innoter_user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from innoter_user.presigned_url import create_presigned_url
from innoter.settings import BUCKET


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token


class ListUserSerializer(serializers.ModelSerializer):
    presigned_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'username', 'email',
                  'role', 'title', 'is_blocked', 'presigned_url')

    @staticmethod
    def get_presigned_url(self):
        if not self.image_s3_path == '':
            seven_days_as_seconds = 604800
            generated_signed_url = create_presigned_url(BUCKET, self.image_s3_path, seven_days_as_seconds)
            return generated_signed_url
        return None


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.JSONField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all()),
                    EmailValidator()]
    )

    password = serializers.JSONField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.JSONField(write_only=True, required=True)
    username = serializers.JSONField(validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.JSONField()
    last_name = serializers.JSONField()
    # role = serializers.JSONField()
    image_s3_path = serializers.JSONField()


    class Meta:
        model = User
        fields = ('pk', 'username', 'password', 'password2', 'email',
                  'first_name', 'last_name', 'role', 'image_s3_path')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'image_s3_path': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            image_s3_path=validated_data['image_s3_path']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'title')

        username = serializers.CharField()


class DetailUserSerializer(serializers.ModelSerializer):
    presigned_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'username', 'email',
                  'role', 'title', 'is_blocked', 'image_s3_path', 'presigned_url')

    @staticmethod
    def get_presigned_url(self):
        if not self.image_s3_path == '':
            seven_days_as_seconds = 604800
            generated_signed_url = create_presigned_url(BUCKET, self.image_s3_path, seven_days_as_seconds)
            return generated_signed_url
        return None


class AttachRoleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'username', 'email',
                  'image_s3_path', 'role', 'title', 'is_blocked')


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()


class UploadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('image_s3_path',)
