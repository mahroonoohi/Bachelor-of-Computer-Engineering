from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from profiles.models import Profile
from users.serializers import LoginInputSerializer, LoginOutputSerializer


class LoginView(APIView):

    @extend_schema(request=LoginInputSerializer, responses=LoginOutputSerializer, tags=['Auth'])
    def post(self, request):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = Profile.objects.get(username=serializer.validated_data['username']).user
        except Profile.DoesNotExist:
            user = None

        if user:
            user = authenticate(username=user.email, password=serializer.validated_data['password'])
        else:
            raise AuthenticationFailed("No active account found with given information.")

        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            output_serializer = LoginOutputSerializer(data=data)
            output_serializer.is_valid(raise_exception=True)
            return Response(output_serializer.validated_data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed("Invalid username/password.")


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER

    @extend_schema(tags=['Auth'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)