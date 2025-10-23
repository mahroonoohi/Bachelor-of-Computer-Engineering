from django.db.models import Model
from rest_framework import serializers
from rest_framework.relations import RelatedField
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str

from idea.models import IdeaReport, Classification, Idea, IdeaLikes, IdeaComment, IdeaAttachmentFile, FinancialStep, \
    SavedIdea, ProfileReport, CollaborationRequest
from profiles.models import Profile


class StringRelatedField(RelatedField):
    default_error_messages = {
        'does_not_exist': _('Object with {string_field}={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }

    def __init__(self, string_field=None, **kwargs):
        assert string_field is not None, 'The `string_field` argument is required.'
        self.string_field = string_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.string_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', string_field=self.string_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, self.string_field)


def inline_model_serializer(*, serializer_model: Model, serializer_name: str, model_fields: list | str,
                            serializer_custom_fields: dict | None = None):
    if serializer_custom_fields:
        serializer_custom_fields['Meta'] = type('Meta', (object,), {"model": serializer_model, 'fields': model_fields})
    else:
        serializer_custom_fields = {
            'Meta': type('Meta', (object,), {"model": serializer_model, 'fields': model_fields})}

    serializer_class = type(serializer_name, (serializers.ModelSerializer,), serializer_custom_fields)

    return serializer_class


class UUIDRelatedField(RelatedField):
    """
    A read-write field that represents the target of the relationship
    by a unique 'slug' attribute.
    """
    default_error_messages = {
        'does_not_exist': _('Object with {uuid_field}={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }

    def __init__(self, uuid_field=None, **kwargs):
        assert uuid_field is not None, 'The `uuid_field` argument is required.'
        self.uuid_field = uuid_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.uuid_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', uuid_field=self.uuid_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, self.uuid_field)


# =========================================================================================================

class IdeaReportInputSerializer(serializers.ModelSerializer):
    idea = serializers.CharField(max_length=40)

    class Meta:
        model = IdeaReport
        fields = ["idea", "report_reasons", "description"]


class ClassificationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = ['uuid', 'title']


class IdeaCreateInputSerializer(serializers.ModelSerializer):
    classification = StringRelatedField(queryset=Classification.objects.all(), string_field='title', many=True)

    class Meta:
        model = Idea
        fields = ['classification', 'title', 'goal', 'abstract', 'description', 'image', 'max_donation',
                  'show_likes', 'show_views', 'show_comments']


class IdeaCreateOutputSerializer(serializers.ModelSerializer):
    classification = StringRelatedField(queryset=Classification.objects.all(), string_field='title', many=True)

    class Meta:
        model = Idea
        fields = ['uuid', 'classification', 'title', 'goal', 'abstract', 'description', 'image', 'max_donation',
                  'show_likes', 'show_views', 'show_comments']


class IdeaDetailOutputSerializer(serializers.ModelSerializer):
    classification = StringRelatedField(queryset=Classification.objects.all(), string_field='title', many=True)
    profile = inline_model_serializer(
        serializer_model=Profile,
        serializer_name="output_idea_detail_profile_serializer",
        model_fields=['username', 'first_name', 'last_name', 'bio', 'follower_count', 'following_count',
                      'idea_count', 'profile_image']
    )()

    class Meta:
        model = Idea
        fields = ['uuid', 'profile', 'classification', 'title', 'goal', 'abstract', 'description', 'image',
                  'max_donation', 'show_likes', 'show_views', 'show_comments', 'views_count', 'likes_count',
                  'comments_count']


class UpdateIdeaInputSerializer(serializers.ModelSerializer):
    classification = StringRelatedField(
        queryset=Classification.objects.all(),
        string_field='title',
        many=True,
        required=False
    )

    class Meta:
        model = Idea
        fields = ['classification', 'title', 'goal', 'abstract', 'description', 'image', 'max_donation',
                  'show_likes', 'show_views', 'show_comments']

        extra_kwargs = dict((x, {'required': False}) for x in fields)


class AttachmentInputSerializer(serializers.Serializer):
    file = serializers.FileField()


class AttachmentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaAttachmentFile
        fields = ['uuid', 'file', 'created_at']


# =========================================================================================================


class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaLikes
        fields = ['profile_id']


class IdeaCommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaComment
        fields = ["comment"]


class IdeaCommentOutputSerializer(serializers.ModelSerializer):
    profile = inline_model_serializer(
        serializer_model=Profile,
        serializer_name="output_idea_comment_profile_serializer",
        model_fields=['username', 'first_name', 'last_name', 'bio', 'follower_count', 'following_count',
                      'idea_count', 'profile_image']
    )()

    class Meta:
        model = IdeaComment
        fields = ["uuid", "date", "profile", "idea", 'comment']


class CreateFinancialStepInputSerializer(serializers.ModelSerializer):
    priority = serializers.IntegerField(max_value=5)

    class Meta:
        model = FinancialStep
        fields = ['title', 'cost', 'description', 'priority', 'unit']


class CreateFinancialStepOutputSerializer(serializers.ModelSerializer):
    idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

    class Meta:
        model = FinancialStep
        fields = ['uuid', 'idea', 'title', 'cost', 'description', 'priority', 'unit']


class UpdateFinancialStepInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialStep
        optional_fields = ['title', 'cost', 'description', 'unit']
        required_fields = []
        fields = [*optional_fields, *required_fields]
        extra_kwargs = dict((x, {'required': False}) for x in optional_fields)


class FinancialStepDetailOutputSerializer(serializers.ModelSerializer):
    idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

    class Meta:
        model = FinancialStep
        fields = ['uuid', 'idea', 'title', 'cost', 'description', 'priority', 'unit']


class IsLikedOutputSerializer(serializers.Serializer):
    is_liked = serializers.BooleanField()


class IsSavedOutputSerializer(serializers.Serializer):
    is_saved = serializers.BooleanField()


class OutputSavedIdeaSerializer(serializers.ModelSerializer):
    idea = inline_model_serializer(
        serializer_model=Idea,
        serializer_name="output_saved_idea_list_idea_serializer",
        model_fields=['uuid', 'profile', 'title', 'abstract', 'goal', 'image', 'views_count', 'likes_count',
                      'comments_count'],
        serializer_custom_fields={
            "profile": inline_model_serializer(
                serializer_model=Profile,
                serializer_name="output_saved_ideas_profile_serializer",
                model_fields=['username', 'first_name', 'last_name', 'bio', 'follower_count', 'following_count',
                              'idea_count', 'profile_image']
            )()
        }
    )()

    class Meta:
        model = SavedIdea
        fields = ['idea', 'date']


# =========================================================================================================


class InputIdeaFilterSerializer(serializers.Serializer):
    classification = StringRelatedField(
        queryset=Classification.objects.all(),
        string_field='title',
        many=True,
        required=False
    )
    usernames = serializers.ListField(child=serializers.CharField(max_length=128), required=False)
    emails = serializers.ListField(child=serializers.EmailField(), required=False)
    sort_by = serializers.ChoiceField(choices=[
        ('views_count', 'views_count'), ('likes_count', 'likes_count'), ('comments_count', 'comments_count'),
        ('created_at', 'created_at')
    ], required=False)

    def validate(self, attrs):
        if attrs.get('usernames', None) and attrs.get('emails', None):
            raise serializers.ValidationError(
                "Only one of 'emails' or 'usernames' fields can be used to apply filter"
            )

        return attrs


class OutputIdeaFilterSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    profile = inline_model_serializer(
        serializer_model=Profile,
        serializer_name="output_idea_filter_profile_serializer",
        model_fields=['username', 'first_name', 'last_name', 'bio', 'follower_count', 'following_count',
                      'idea_count', 'profile_image']
    )()

    class Meta:
        model = Idea
        fields = ['uuid', 'profile', 'title', 'abstract', 'goal', 'image', 'views_count', 'likes_count',
                  'comments_count']

    def get_views_count(self, idea):
        if idea.show_views:
            return idea.views_count
        return None

    def get_likes_count(self, idea):
        if idea.show_likes:
            return idea.likes_count
        return None

    def get_comments_count(self, idea):
        if idea.show_comments:
            return idea.comments_count
        return None


class InputUserIdeaFilterSerializer(serializers.Serializer):
    classification = StringRelatedField(
        queryset=Classification.objects.all(),
        string_field='title',
        many=True,
        required=False
    )
    sort_by = serializers.ChoiceField(choices=[
        ('views_count', 'views_count'), ('likes_count', 'likes_count'), ('comments_count', 'comments_count'),
        ('created_at', 'created_at')
    ], required=False)


class OutputUserIdeaFilterSerializer(serializers.ModelSerializer):
    profile = inline_model_serializer(
        serializer_model=Profile,
        serializer_name="output_user_idea_filter_profile_serializer",
        model_fields=['username', 'first_name', 'last_name', 'bio', 'follower_count', 'following_count',
                      'idea_count', 'profile_image']
    )()

    class Meta:
        model = Idea
        fields = ['uuid', 'profile', 'title', 'goal', 'abstract', 'image', 'views_count', 'likes_count',
                  'comments_count']


class InputProfileReportSerializer(serializers.ModelSerializer):
    profile_username = serializers.CharField(max_length=128)

    class Meta:
        model = ProfileReport
        fields = ["profile_username", "report_reasons", "description"]

    # =========================================================================================================

class InputUpdateCollaborationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaborationRequest
        optional_fields = ['title', 'status', 'skills', 'age', 'description', 'education', 'salary']
        required_fields = []
        fields = [*optional_fields, *required_fields]
        extra_kwargs = dict((x, {'required': False}) for x in optional_fields)

class OutputCollaborationRequestDetailSerializer(serializers.ModelSerializer):
    idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

    class Meta:
        model = CollaborationRequest
        fields = ['uuid', 'title', 'status', 'idea', 'skills', 'age', 'description', 'education', 'salary']



class InputIdeaCollaborationRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollaborationRequest
        fields = ['title', 'status', 'skills', 'age', 'education', 'description', 'salary']

class OutputCollaborationRequestSerializer(serializers.ModelSerializer):
    idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

    class Meta:
        model = CollaborationRequest
        fields = ['title', 'status', 'uuid', 'idea', 'skills', 'age', 'description', 'education', 'salary']