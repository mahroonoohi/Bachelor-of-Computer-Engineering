from django.shortcuts import render

# Create your views here.
from django.db import IntegrityError
from django.db.models import Model, QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Sequence, Type, TYPE_CHECKING
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from idea.models import Idea, IdeaReport, Classification, IdeaLikes, IdeaComment, IdeaAttachmentFile, FinancialStep, \
    SavedIdea, ProfileReport, CollaborationRequest, IdeaViews
from idea.serializers import IdeaReportInputSerializer, ClassificationOutputSerializer, IdeaCreateInputSerializer, \
    IdeaCreateOutputSerializer, IdeaDetailOutputSerializer, UpdateIdeaInputSerializer, UserLikeSerializer, \
    IdeaCommentOutputSerializer, IdeaCommentInputSerializer, AttachmentInputSerializer, AttachmentOutputSerializer, \
    CreateFinancialStepOutputSerializer, CreateFinancialStepInputSerializer, UpdateFinancialStepInputSerializer, \
    FinancialStepDetailOutputSerializer, IsLikedOutputSerializer, OutputSavedIdeaSerializer, IsSavedOutputSerializer, \
    InputIdeaFilterSerializer, OutputIdeaFilterSerializer, InputUserIdeaFilterSerializer, \
    OutputUserIdeaFilterSerializer, InputProfileReportSerializer, InputUpdateCollaborationRequestSerializer, \
    OutputCollaborationRequestDetailSerializer, OutputCollaborationRequestSerializer, \
    InputIdeaCollaborationRequestSerializer
from profiles.models import Profile
from rest_framework.utils import model_meta

MAX_FILE_ATTACHMENT_COUNT = 3


def update_model_instance(*, instance: Model, data: dict) -> Model:
    """Updates given model instance using given data"""
    info = model_meta.get_field_info(instance)

    many_to_many_fields = []
    for attr, value in data.items():
        if attr in info.relations and info.relations[attr].to_many:
            many_to_many_fields.append((attr, value))
        else:
            setattr(instance, attr, value)

    instance.save()

    for attr, value in many_to_many_fields:
        field = getattr(instance, attr)
        field.set(value)

    return instance


# =========================================================================================================


class IdeaReportAPI(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=IdeaReportInputSerializer, tags=["Reports"])
    def post(self, request):
        idea_report = IdeaReportInputSerializer(data=request.data)
        idea_report.is_valid(raise_exception=True)
        reporter_profile = Profile.objects.get(user=request.user)

        data = idea_report.validated_data
        try:
            temp = Idea.objects.filter(uuid=data.pop('idea'))

            if temp.exists():
                idea = temp.first()
            else:
                idea = None

            if not idea:
                raise ValueError("idea doesn't exists")
            idea_report = IdeaReport.objects.create(reporter=reporter_profile, idea=idea, **data)

        except ValueError as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class ClassificationAPI(APIView):

    @extend_schema(responses=ClassificationOutputSerializer(many=True), tags=['Classification'])
    def get(self, request):
        classifications = Classification.objects.all()
        serializer = ClassificationOutputSerializer(instance=classifications, many=True)
        return Response(data=serializer.data)


class IdeaCreateAPI(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=IdeaCreateInputSerializer, responses=IdeaCreateOutputSerializer, tags=['Idea'])
    def post(self, request):
        serializer = IdeaCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = Profile.objects.get(user=request.user)

        data = serializer.validated_data

        classification = data.pop('classification')
        idea = Idea.objects.create(profile=profile, **data)
        idea.classification.set(classification)

        output_serializer = IdeaCreateOutputSerializer(instance=idea)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class IdeaDetailView(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=IdeaDetailOutputSerializer, tags=['Idea'])
    def get(self, request, idea_uuid):
        idea = Idea.objects.filter(uuid=idea_uuid)
        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)
        serializer = IdeaDetailOutputSerializer(instance=idea)

        IdeaViews.objects.create(user=request.user, idea=idea)

        return Response(data=serializer.data)

    @extend_schema(request=UpdateIdeaInputSerializer, responses=IdeaDetailOutputSerializer, tags=['Idea'])
    def put(self, request, idea_uuid):
        serializer = UpdateIdeaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idea = Idea.objects.filter(uuid=idea_uuid, profile__user=request.user)
        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        updated_idea = update_model_instance(instance=idea, data=serializer.validated_data)

        serializer = IdeaDetailOutputSerializer(instance=updated_idea)
        return Response(data=serializer.data)

    @extend_schema(tags=['Idea'])
    def delete(self, request, idea_uuid):

        idea = Idea.objects.filter(uuid=idea_uuid, profile__user=request.user)
        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        idea.delete()
        return Response(status=status.HTTP_200_OK)


class IdeaAttachmentApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=AttachmentOutputSerializer(many=True), tags=["Attachments"])
    def get(self, request, idea_uuid):

        idea = Idea.objects.filter(uuid=idea_uuid)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        attachments = IdeaAttachmentFile.objects.filter(idea=idea)
        serializer = AttachmentOutputSerializer(instance=attachments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=AttachmentInputSerializer, responses=AttachmentOutputSerializer, tags=["Attachments"])
    def post(self, request, idea_uuid):
        serializer = AttachmentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idea = Idea.objects.filter(uuid=idea_uuid, profile__user=request.user)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        if idea.attached_files_count >= MAX_FILE_ATTACHMENT_COUNT:
            attachment = None

        attachment = IdeaAttachmentFile.objects.create(idea=idea, **serializer.validated_data)
        idea.attached_files_count += 1
        idea.save()

        if not attachment:
            return Response("Maximum number of attachment reached!", status=status.HTTP_403_FORBIDDEN)

        output_serializer = AttachmentOutputSerializer(instance=attachment)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class IdeaAttachmentDetailApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["Attachments"])
    def delete(self, request, attachment_uuid):

        attachment = IdeaAttachmentFile.objects.filter(uuid=attachment_uuid, idea__profile__user=request.user)

        if attachment.exists():
            attachment = attachment.first()
        else:
            attachment = None

        if not request:
            return Response("No attachment found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        attachment.delete()
        return Response(status=status.HTTP_200_OK)


# =========================================================================================================


class IdeaFinancialStepApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=CreateFinancialStepOutputSerializer(many=True), tags=['Financial Step'])
    def get(self, request, idea_uuid):

        idea = Idea.objects.filter(uuid=idea_uuid)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        steps = FinancialStep.objects.filter(idea=idea)
        serializer = CreateFinancialStepOutputSerializer(instance=steps, many=True)
        return Response(data=serializer.data)

    @extend_schema(request=CreateFinancialStepInputSerializer(many=True),
                   responses=CreateFinancialStepOutputSerializer(many=True),
                   tags=['Financial Step'])
    def post(self, request, idea_uuid):

        idea = Idea.objects.filter(uuid=idea_uuid, profile__user=request.user)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        serializer = CreateFinancialStepInputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        created_steps = []

        for data in serializer.validated_data:

            try:
                step = FinancialStep.objects.create(idea=idea, **data)
            except IntegrityError:
                step = None

            if step:
                created_steps.append(step)
            else:
                return Response(f"invalid priority: {data['priority']}", status=status.HTTP_400_BAD_REQUEST)

        output_serializer = CreateFinancialStepOutputSerializer(instance=created_steps, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class IdeaFinancialDetailApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=UpdateFinancialStepInputSerializer,
                   responses=FinancialStepDetailOutputSerializer,
                   tags=['Financial Step'])
    def put(self, request, financial_uuid):
        serializer = UpdateFinancialStepInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        step = FinancialStep.objects.filter(uuid=financial_uuid, idea__profile__user=request.user)

        if step.exists():
            step = step.first()
        else:
            step = None

        if not step:
            return Response("No financial step found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        updated_step = update_model_instance(instance=step, data=serializer.validated_data)

        output_serializer = FinancialStepDetailOutputSerializer(instance=updated_step)
        return Response(data=output_serializer.data)

    @extend_schema(tags=['Financial Step'])
    def delete(self, request, financial_uuid):

        step = FinancialStep.objects.filter(uuid=financial_uuid, idea__profile__user=request.user)

        if step.exists():
            step = step.first()
        else:
            step = None

        if not step:
            return Response("No financial step with this uuid!", status=status.HTTP_404_NOT_FOUND)

        step.delete()
        return Response(status=status.HTTP_200_OK)


class IdeaLikeApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=UserLikeSerializer(many=True), tags=['Idea Like'])
    def get(self, request, idea_uuid):
        queryset = IdeaLikes.objects.filter(idea_id__uuid=idea_uuid)
        serializer = UserLikeSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(tags=['Idea Like'])
    def post(self, request, idea_uuid):
        idea = Idea.objects.get(uuid=idea_uuid)
        profile = Profile.objects.get(user=request.user)

        temp = IdeaLikes.objects.filter(idea_id=idea, profile_id=profile)

        if temp.exists():
            temp.delete()
            idea.likes_count -= 1
            idea.save()
            return Response(data={"is_like": False}, status=status.HTTP_200_OK)
        else:
            temp = IdeaLikes.objects.create(idea_id=idea, profile_id=profile)
            idea.likes_count += 1
            idea.save()
            return Response(data={"is_like": True}, status=status.HTTP_200_OK)


class IsLikedApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=IsLikedOutputSerializer, tags=['Idea Like'])
    def get(self, request, idea_uuid):
        profile = Profile.objects.get(user=request.user)
        queryset = IdeaLikes.objects.filter(profile_id=profile, idea_id__uuid=idea_uuid)

        serializer = IsLikedOutputSerializer(instance={"is_liked": queryset.exists()})
        return Response(serializer.data)


class IdeaCommentApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=IdeaCommentOutputSerializer(many=True), tags=["Comments"])
    def get(self, request, idea_uuid):

        idea = Idea.objects.filter(uuid=idea_uuid)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        if not idea.show_comments:
            return Response(data={'message': "Idea's comments are hidden"}, status=status.HTTP_403_FORBIDDEN)

        if not idea.show_comments:
            return Response(data=[], status=status.HTTP_200_OK)

        comments = IdeaComment.objects.filter(idea=idea)
        serializer = IdeaCommentOutputSerializer(instance=comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=IdeaCommentInputSerializer, responses=IdeaCommentOutputSerializer, tags=["Comments"])
    def post(self, request, idea_uuid):
        serializer = IdeaCommentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idea = Idea.objects.filter(uuid=idea_uuid)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        profile = Profile.objects.get(user=request.user)

        comment = IdeaComment.objects.create(idea=idea, profile=profile, **serializer.validated_data)
        idea.comments_count += 1
        idea.save()

        output_serializer = IdeaCommentOutputSerializer(instance=comment)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


# =========================================================================================================


class SaveIdeaApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=['Saved Ideas'])
    def post(self, request, idea_uuid):
        profile = Profile.objects.get(user=request.user)
        idea = Idea.objects.filter(uuid=idea_uuid)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        temp = SavedIdea.objects.filter(profile=profile, idea=idea)
        if temp.exists():
            temp.delete()
            return Response(data={"is_saved": False}, status=status.HTTP_200_OK)

        else:
            SavedIdea.objects.create(profile=profile, idea=idea)
            return Response(data={"is_saved": True}, status=status.HTTP_200_OK)


class SavedIdeaListApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=OutputSavedIdeaSerializer(many=True), tags=['Saved Ideas'])
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        saved_ideas = SavedIdea.objects.filter(profile=profile)
        serializer = OutputSavedIdeaSerializer(instance=saved_ideas, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class IsSavedApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=IsSavedOutputSerializer, tags=['Saved Ideas'])
    def get(self, request, idea_uuid):
        profile = Profile.objects.get(user=request.user)
        queryset = SavedIdea.objects.filter(profile=profile, idea__uuid=idea_uuid)

        serializer = IsSavedOutputSerializer(instance={"is_saved": queryset.exists()})
        return Response(serializer.data)


# =========================================================================================================


def filter_ideas(
        classification: list = None, usernames: list = None, emails: list = None, sort_by: str = 'created_at'
) -> QuerySet(Idea):
    search_params = {"profile__is_public": True}

    if classification:
        search_params["classification__in"] = classification

    if usernames:
        search_params["profile__username__in"] = usernames

    if emails:
        search_params["profile__user__email__in"] = emails

    return Idea.objects.filter(**search_params).order_by(f"-{sort_by}")


def user_filter_ideas(
        profile: Profile, classification: list = None, sort_by: str = 'created_at'
) -> QuerySet(Idea):
    search_params = {"profile": profile}

    if classification:
        search_params["classification__in"] = classification

    return Idea.objects.filter(**search_params).order_by(f"-{sort_by}")



def user_filter_saved_ideas(
        profile: Profile, classification: list = None, sort_by: str = 'created_at'
) -> QuerySet(Idea):
    search_params = {"savedidea__profile": profile}

    if classification:
        search_params["classification__in"] = classification

    return Idea.objects.filter(**search_params).order_by(f"-{sort_by}")


class IdeaFilterApi(APIView):

    @extend_schema(request=InputIdeaFilterSerializer, responses=OutputIdeaFilterSerializer(many=True), tags=['Filter'])
    def post(self, request):
        serializer = InputIdeaFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ideas = filter_ideas(**serializer.validated_data)

        output_serializer = OutputIdeaFilterSerializer(instance=ideas, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)


class UserIdeaFilterApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=InputUserIdeaFilterSerializer, responses=OutputUserIdeaFilterSerializer(many=True),
                   tags=['Filter'])
    def post(self, request):
        serializer = InputUserIdeaFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = Profile.objects.get(user=request.user)

        ideas = user_filter_ideas(profile=profile, **serializer.validated_data)

        output_serializer = OutputUserIdeaFilterSerializer(instance=ideas, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)



class UserSavedIdeaFilterApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=InputUserIdeaFilterSerializer, responses=OutputUserIdeaFilterSerializer(many=True),
                   tags=['Filter'])
    def post(self, request):
        serializer = InputUserIdeaFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = Profile.objects.get(user=request.user)

        ideas = user_filter_saved_ideas(profile=profile, **serializer.validated_data)

        output_serializer = OutputUserIdeaFilterSerializer(instance=ideas, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)


class ProfileReportAPI(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=InputProfileReportSerializer, tags=["Reports"])
    def post(self, request):
        profile_report = InputProfileReportSerializer(data=request.data)
        profile_report.is_valid(raise_exception=True)
        reporter_profile = Profile.objects.get(user=request.user)
        try:
            data = profile_report.validated_data

            reported_profile = Profile.objects.filter(username=data.pop("profile_username"))
            if reported_profile.exists():
                reported_profile = reported_profile.first()
            else:
                reported_profile = None

            if not reported_profile:
                raise ValueError("profile_username doesn't exists")
            profile_report = ProfileReport.objects.create(reporter_id=reporter_profile, profile_id=reported_profile,
                                                          **data)



        except ValueError as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


# =========================================================================================================


class IdeaCollaborationRequestApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=OutputCollaborationRequestSerializer(many=True), tags=['Collaboration Request'])
    def get(self, request, idea_uuid):

        idea = Idea.objects.filter(uuid=idea_uuid)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)
        collaboration_request = CollaborationRequest.objects.filter(idea=idea)
        serializer = OutputCollaborationRequestSerializer(instance=collaboration_request, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=InputIdeaCollaborationRequestSerializer(),
                   responses=OutputCollaborationRequestSerializer(),
                   tags=['Collaboration Request'])
    def post(self, request, idea_uuid):

        idea = Idea.objects.filter(uuid=idea_uuid, profile__user=request.user)

        if idea.exists():
            idea = idea.first()
        else:
            idea = None

        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        serializer = InputIdeaCollaborationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_collaboration_request = CollaborationRequest.objects.create(idea=idea, **serializer.validated_data)

        output_serializer = OutputCollaborationRequestSerializer(instance=new_collaboration_request)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class IdeaCollaborationRequestDetailApi(APIView):
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JWTAuthentication,
    ]
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=InputUpdateCollaborationRequestSerializer,
                   responses=OutputCollaborationRequestDetailSerializer,
                   tags=['Collaboration Request'])
    def put(self, request, collaboration_request_uuid):
        serializer = InputUpdateCollaborationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        collab_request = CollaborationRequest.objects.filter(
            uuid=collaboration_request_uuid,
            idea__profile__user=request.user
        )

        if collab_request.exists():
            collab_request = collab_request.first()
        else:
            collab_request = None

        if not collab_request:
            return Response("No collaboration request found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        updated_request = update_model_instance(instance=collab_request, data=serializer.validated_data)
        output_serializer = OutputCollaborationRequestDetailSerializer(instance=updated_request)
        return Response(data=output_serializer.data)

    @extend_schema(tags=['Collaboration Request'])
    def delete(self, request, collaboration_request_uuid):

        collab_request = CollaborationRequest.objects.filter(
            uuid=collaboration_request_uuid,
            idea__profile__user=request.user
        )

        if collab_request.exists():
            collab_request = collab_request.first()
        else:
            collab_request = None

        if not collab_request:
            return Response("No collaboration request with this uuid!", status=status.HTTP_404_NOT_FOUND)

        collab_request.delete()
        return Response(status=status.HTTP_200_OK)
