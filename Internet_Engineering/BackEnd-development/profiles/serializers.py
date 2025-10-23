from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from idea.serializers import inline_model_serializer
from profiles.models import Address, Profile, ProfileLinks
from users.models import BaseUser


class RegisterInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=256, validators=[MinLengthValidator(limit_value=8)])

    def validate_email(self, email):
        base_user = None
        try:
            base_user = BaseUser.objects.get(email=email)
        except BaseUser.DoesNotExist:
            pass

        if base_user:
            raise serializers.ValidationError("Email exists")

        return email


class RegisterOutputSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = BaseUser
        fields = ("token", "created_at")

    def get_token(self, user):
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class IsFollowdedOutputSerializer(serializers.Serializer):
    is_followed = serializers.BooleanField()


# ===========================================================================================

class OutPutUserProfileSerializer(serializers.ModelSerializer):
    user = inline_model_serializer(
        serializer_model=BaseUser,
        serializer_name='output_user_profile_user',
        model_fields=['email']
    )()

    address = inline_model_serializer(
        serializer_name="user_profile_address_serializer",
        serializer_model=Address,
        model_fields=[
            'country', 'state', 'city', 'address', 'zip_code'
        ]
    )()

    class Meta:
        model = Profile
        fields = (
        'user', "username", "profile_image", "first_name", "last_name", "gender", "birth_date", "address", "bio"
        , "follower_count", "following_count", "idea_count", "is_public", "is_active", "is_banned")


class InputUpdateUserProfileSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=256,
        validators=[
            MinLengthValidator(limit_value=8)
        ],
        required=False
    )
    new_password = serializers.CharField(
        max_length=256,
        validators=[
            MinLengthValidator(limit_value=8)
        ],
        required=False
    )

    address = inline_model_serializer(
        serializer_name="user_profile_edit_address_serializer",
        serializer_model=Address,
        model_fields=[
            'country', 'state', 'city', 'address', 'zip_code'
        ]
    )(required=False)

    class Meta:
        model = Profile
        optional_fields = ['username', 'first_name', 'last_name', 'birth_date', 'gender', 'bio', 'address',
                           'profile_image',
                           'is_public', 'old_password', 'new_password']
        required_fields = []
        fields = [*optional_fields, *required_fields]

        extra_kwargs = dict((x, {'required': False}) for x in optional_fields)

    def validate(self, attrs):
        super().validate(attrs=attrs)
        if attrs.get('new_password', None) and attrs.get('old_password', None) is None:
            raise serializers.ValidationError("You must enter old password")

        return super().validate(attrs=attrs)

    def validate_username(self, username):
        profile = Profile.objects.filter(username=username)
        if profile:
            raise serializers.ValidationError("This username is already exists")

        return username


class OutputGeneralUserProfileSerializer(serializers.ModelSerializer):
    user = inline_model_serializer(
        serializer_model=BaseUser,
        serializer_name='output_general_user_profile_user',
        model_fields=['email']
    )()

    address = inline_model_serializer(
        serializer_name="general_user_profile_address_serializer",
        serializer_model=Address,
        model_fields=[
            'country', 'state', 'city', 'address', 'zip_code'
        ]
    )()

    class Meta:
        model = Profile
        fields = ('user', "username", "profile_image", "first_name", "last_name", "gender", "birth_date", "address"
                  , "bio", "follower_count", "following_count", "idea_count")




class OutputFollowerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'profile_image', 'follower_count', 'following_count',
                  'idea_count']




class OutputFollowingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'profile_image', 'follower_count', 'following_count',
                  'idea_count']




class InputSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLinks
        fields = ['type', 'link']

class OutputSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLinks
        fields = ['uuid', 'type', 'link']



class InputChangePasswordSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=128, required=False)
        validation_code = serializers.CharField(max_length=6)
        new_password = serializers.CharField(
            max_length=256,
            validators=[
                MinLengthValidator(limit_value=8)
            ]
        )


class InputForgetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, required=False)