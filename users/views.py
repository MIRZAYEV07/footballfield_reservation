from django.contrib.auth import get_user_model
from rest_framework import generics, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password

from common import permissions

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import MyTokenObtainPairSerializer, UserSerializer, AuthTokenSerializer, UserDetailSerializer, \
    UserUpdateSerializer, UserRegistrationSerializer, UserLoginSerializer

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ["username"]


user_list_view = UserListAPIView.as_view()


class UserObtainTokenAPIView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.AdminRenderer)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(instance=user)
        details = user_serializer.data
        details.update(token=token.key)
        return Response(details)


user_login_view = UserObtainTokenAPIView.as_view()


class LogoutAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={"message": "You have successfully logged out"},
        )


user_logout_view = LogoutAPIView.as_view()


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "guid"


user_detail_api_view = UserDetailAPIView.as_view()


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.UpdatePermission]
    lookup_field = "guid"


user_update_api_view = UserUpdateAPIView.as_view()


class AuthUserRegistrationView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User succesfully registered',
                'user': serializer.data
            }

            return Response(response, status=status_code)


user_registration_api_view = AuthUserRegistrationView.as_view()


class AuthUserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                }
            }

            return Response(response, status=status_code)


user_login_api_view = AuthUserLoginView.as_view()

