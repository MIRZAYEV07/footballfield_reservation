import re

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def validate_username(username):

    if len(username) < 5:
        raise serializers.ValidationError("Username must be at least 3 characters long.")
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise serializers.ValidationError("Username must consist of alphanumeric characters and underscores only.")
    if User.objects.filter(username=username).exists():
        raise serializers.ValidationError("Username is already taken.")

    return username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "guid",
            "username",
            "first_name",
        )


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("username"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")


        try:
            validate_username(username)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"username": e.detail})


        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "guid",
            "first_name",
            "username",

        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "guid",
            "first_name",

        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "guid",
            'first_name',
            'username',
            'password',

        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['id'] = self.user.id
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['guid'] = self.user.guid

        return data



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': _('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail(_('bad_token'))