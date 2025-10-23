from random import choice
from string import ascii_uppercase, digits

from django.conf import settings
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Sequence, Type, TYPE_CHECKING
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from idea.views import update_model_instance
from profiles.models import Profile, Follow, Address, ProfileLinks
from profiles.serializers import RegisterInputSerializer, RegisterOutputSerializer, IsFollowdedOutputSerializer, \
    OutPutUserProfileSerializer, InputUpdateUserProfileSerializer, OutputGeneralUserProfileSerializer, \
    OutputFollowerProfileSerializer, OutputFollowingProfileSerializer, OutputSocialMediaSerializer, \
    InputSocialMediaSerializer, InputForgetPasswordSerializer, InputChangePasswordSerializer
from users.models import BaseUser
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.http import HttpResponse

from users.tasks import send_email_confirmation_link, send_email_password_confirmation


# Create your views here.


class InvalidPassword(Exception):
    pass


@never_cache
def verify_email(request, username, token):
    email_verify = cache.get(f"email_verification__{username}")
    if email_verify and email_verify[0] == token:
        user = Profile.objects.get(username=username).user
        user.is_email_verified = True
        user.save()
        cache.delete(f"email_verification__{username}")
        return HttpResponse("Your email has been successfully verified")

    elif email_verify and email_verify[0] != token:
        if email_verify[1] >= 3:
            cache.delete(f"email_verification__{username}")
        else:
            cache.set(
                f"email_verification__{username}",
                (email_verify[0], email_verify[1] + 1),
                cache.ttl(f"email_verification__{username}")
            )
        return HttpResponse("Invalid verification URL!")

    return HttpResponse("Invalid Token!")


class RegisterApi(APIView):

    @extend_schema(request=RegisterInputSerializer, responses=RegisterOutputSerializer, tags=['User'])
    def post(self, request):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data: dict = serializer.validated_data

        user = BaseUser.objects.create_user(email=validated_data.pop('email'), password=validated_data.pop('password'))

        try:
            profile = Profile.objects.create(
                username=validated_data.pop('username'),
                user=user
            )
        except IntegrityError:
            return Response(data={"details": {"username": ["Username exists"]}})

        send_email_confirmation_link.delay(user.email, user.id, profile.username)

        output_serializer = RegisterOutputSerializer(instance=user)

        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class FollowApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=['Follow'])
    def post(self, request, username):

        try:
            following = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return Response(
                data={"detail": {"username": ["No user found with this username"]}},
                status=status.HTTP_404_NOT_FOUND
            )

        follower = Profile.objects.get(user=request.user)

        temp = Follow.objects.filter(follower=follower, following=following)

        if temp.exists():
            temp.delete()
            return Response(data={"is_follow": False}, status=status.HTTP_200_OK)

        else:
            Follow.objects.create(follower=follower, following=following)

            follower.following_count += 1
            following.follower_count += 1
            follower.save()
            following.save()
            return Response(data={"is_follow": True}, status=status.HTTP_200_OK)


class IsFollowedApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=IsFollowdedOutputSerializer, tags=['Follow'])
    def get(self, request, username):
        following = Profile.objects.get(username=username)
        follower = Profile.objects.get(user=request.user)

        temp = Follow.objects.filter(follower=follower, following=following)

        serializer = IsFollowdedOutputSerializer(instance={"is_followed": temp.exists()})
        return Response(serializer.data)


# ===========================================================================================


class UserProfileApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=OutPutUserProfileSerializer, tags=['User'])
    def get(self, request):
        query = Profile.objects.get(user=request.user)
        return Response(OutPutUserProfileSerializer(instance=query).data)

    @extend_schema(request=InputUpdateUserProfileSerializer, responses=OutPutUserProfileSerializer, tags=['User'])
    def put(self, request):
        serializer = InputUpdateUserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = Profile.objects.get(user=request.user)

        try:

            data = serializer.validated_data

            if data.get('new_password', None):
                user = authenticate(email=profile.user.email, password=data['old_password'])
                if user:
                    user.set_password(data['new_password'])
                    user.save()
                else:
                    raise InvalidPassword("Invalid password")

            new_address = data.get('address', None)

            if new_address and profile.address is not None:
                updated_address = update_model_instance(instance=profile.address, data=new_address)
                data.pop('address')

            elif new_address and profile.address is None:
                address = Address.objects.create(**new_address)
                profile.address = address
                profile.save()
                data.pop('address')

            updated_profile = update_model_instance(instance=profile, data=data)


        except InvalidPassword as ex:
            return Response("Invalid old password", status=status.HTTP_400_BAD_REQUEST)

        update_serializer = OutPutUserProfileSerializer(instance=updated_profile)
        return Response(data=update_serializer.data)


class GeneralProfileApi(APIView):

    @extend_schema(responses=OutputGeneralUserProfileSerializer, tags=['User'])
    def get(self, request, username):
        try:
            query = Profile.objects.get(username=username, is_active=True, is_banned=False, is_public=True)
        except Profile.DoesNotExist:
            query = None

        if not query:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        return Response(OutputGeneralUserProfileSerializer(instance=query).data)


class UserProfileFollowerListApi(APIView):

    @extend_schema(responses=OutputFollowerProfileSerializer(many=True), tags=['Follow'])
    def get(self, request, username):

        profiles = Profile.objects.filter(username=username)
        if profiles.exists():
            profile = profiles.first()
        else:
            profile = None

        if not profile:
            return Response(data={'details': {"username": ["No profile found with this username"]}}
                            , status=status.HTTP_404_NOT_FOUND)

        temp = Follow.objects.filter(following=profile)
        followers = [x.follower for x in temp]

        output_serializer = OutputFollowerProfileSerializer(instance=followers, many=True)
        return Response(data=output_serializer.data)


class UserProfileFollowingListApi(APIView):

    @extend_schema(responses=OutputFollowingProfileSerializer(many=True), tags=['Follow'])
    def get(self, request, username):
        profiles = Profile.objects.filter(username=username)
        if profiles.exists():
            profile = profiles.first()
        else:
            profile = None

        if not profile:
            return Response(data={'details': {"username": ["No profile found with this username"]}}
                            , status=status.HTTP_404_NOT_FOUND)

        temp = Follow.objects.filter(follower=profile)
        followers = [x.following for x in temp]

        output_serializer = OutputFollowingProfileSerializer(instance=followers, many=True)
        return Response(data=output_serializer.data)


class UserProfileSocialMediaApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=OutputSocialMediaSerializer(many=True), tags=['Social Media'])
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        social_media = ProfileLinks.objects.filter(profile=profile)
        serializer = OutputSocialMediaSerializer(instance=social_media, many=True)
        return Response(data=serializer.data)

    @extend_schema(request=InputSocialMediaSerializer, responses=OutputSocialMediaSerializer, tags=['Social Media'])
    def post(self, request):
        serializer = InputSocialMediaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = Profile.objects.get(user=request.user)

        try:
            link = ProfileLinks(profile=profile, **serializer.validated_data)
            link.full_clean()
            link.save()
        except IntegrityError:
            link = None

        if not link:
            return Response(
                data={'details': {'type': ["this social media type is already exists for this user"]}},
                status=status.HTTP_400_BAD_REQUEST
            )

        output_serializer = OutputSocialMediaSerializer(instance=link)
        return Response(data=output_serializer.data)


class UserProfileSocialMediaDetailApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=['Social Media'])
    def delete(self, request, social_media_uuid):
        profile = Profile.objects.get(user=request.user)
        try:
            social_media = ProfileLinks.objects.get(uuid=social_media_uuid, profile=profile)
        except:
            return Response(
                data={'details': {'social_media_uuid': ["No social media found with given uuid for this user"]}},
                status=status.HTTP_404_NOT_FOUND
            )

        social_media.delete()
        return Response(status=status.HTTP_200_OK)


def send_password_change_verification_code(*, username):
    profiles = Profile.objects.filter(username=username)
    if profiles.exists():
        profile = profiles.first()
    else:
        profile = None

    if not profile:
        raise ValueError('Invalid username')

    # validation_code = ''.join(choice(ascii_uppercase+digits) for i in range(4))
    validation_code = "1111"
    user = profile.user

    cache.set(f"change_password__{username}", [validation_code.lower(), 0], 3 * 60)

    send_email_password_confirmation.delay(user_id=user.id, username=profile.username, validation_code=validation_code)


def change_password(*, username: str, validation_code: str, new_password: str) -> bool:
    profiles = Profile.objects.filter(username=username)
    if profiles.exists():
        profile = profiles.first()
    else:
        profile = None

    if not profile:
        raise ValueError('Invalid username')

    cached_validation_code = cache.get(f"change_password__{username}")

    if cached_validation_code is None:
        return False

    if cached_validation_code[1] >= 3:
        return False

    if cached_validation_code[0] != validation_code.lower():
        cache.set(
            f"change_password__{username}",
            [cached_validation_code[0], cached_validation_code[1] + 1],
            cache.ttl(f"change_password__{username}")
        )

    user = profile.user
    user.set_password(new_password)
    user.save()

    cache.delete(f"change_password__{username}")

    return True


class ForgetPasswordApi(APIView):

    @extend_schema(request=InputForgetPasswordSerializer, tags=["Forget Password"])
    def post(self, request):
        serializer = InputForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            send_password_change_verification_code(**serializer.validated_data)
        except ValueError:
            return Response("invalid username", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class ChangePasswordApi(APIView):

    @extend_schema(request=InputChangePasswordSerializer, tags=["Forget Password"])
    def post(self, request):
        serializer = InputChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_changed = change_password(**serializer.validated_data)
        if is_changed:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
