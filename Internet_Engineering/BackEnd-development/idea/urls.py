from django.urls import path

from .views import ClassificationAPI, IdeaCreateAPI, IdeaDetailView, IdeaFinancialStepApi, IdeaFinancialDetailApi, \
    IdeaCommentApi, IdeaAttachmentDetailApi, IdeaAttachmentApi, IdeaLikeApi, IdeaFilterApi, \
    UserIdeaFilterApi, SaveIdeaApi, SavedIdeaListApi, IdeaReportAPI, ProfileReportAPI, IsLikedApi, IsSavedApi, \
    IdeaCollaborationRequestApi, IdeaCollaborationRequestDetailApi, UserSavedIdeaFilterApi

urlpatterns = [
    path('idea/classification/list', ClassificationAPI.as_view(), name="classification-list"),
    path('idea/create', IdeaCreateAPI.as_view(), name="idea-create"),
    path('idea/detail/<str:idea_uuid>', IdeaDetailView.as_view(), name='idea-detail'),
    path('idea/financial/<str:idea_uuid>', IdeaFinancialStepApi.as_view(), name='idea-financial'),

    path('idea/like/<str:idea_uuid>', IdeaLikeApi.as_view(), name='Idea-like'),
    path('idea/is-like/<str:idea_uuid>', IsLikedApi.as_view(), name='is-Idea-like'),

    path('idea/financial/detail/<str:financial_uuid>', IdeaFinancialDetailApi.as_view(), name='financial-detail'),
    path('idea/comment/<str:idea_uuid>', IdeaCommentApi.as_view(), name='idea-comment'),
    path('idea/attachment/<str:idea_uuid>', IdeaAttachmentApi.as_view(), name='idea-attachment'),
    path('idea/attachment/detail/<str:attachment_uuid>', IdeaAttachmentDetailApi.as_view(), name='attachment-detail'),
    path('idea/filter/', IdeaFilterApi.as_view(), name='idea-filter'),
    path('idea/filter/user/', UserIdeaFilterApi.as_view(), name='user-idea-filter'),
    path('idea/filter/saved/', UserSavedIdeaFilterApi.as_view(), name='user-saved-idea-filter'),


    path('idea/save-idea/<str:idea_uuid>', SaveIdeaApi.as_view(), name='save-idea'),
    path('idea/is-save-idea/<str:idea_uuid>', IsSavedApi.as_view(), name='is-save-idea'),
    path('idea/save-idea/', SavedIdeaListApi.as_view(), name='save-idea-list'),

    path('idea/collaboration/<str:idea_uuid>', IdeaCollaborationRequestApi.as_view(), name='idea-collaboration request'),
    path('idea/collaboration/detail/<str:collaboration_request_uuid>', IdeaCollaborationRequestDetailApi.as_view(),
         name='collaboration-request-detail'),


    path('report/idea/', IdeaReportAPI.as_view(), name="IdeaReport"),
    path('report/profile/', ProfileReportAPI.as_view(), name="ProfileReport"),

]
