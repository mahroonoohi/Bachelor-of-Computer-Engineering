from django.urls import path

from profiles.views import RegisterApi, FollowApi, verify_email, IsFollowedApi, UserProfileFollowingListApi, \
    GeneralProfileApi, UserProfileApi, UserProfileFollowerListApi, UserProfileSocialMediaApi, \
    UserProfileSocialMediaDetailApi, ForgetPasswordApi, ChangePasswordApi

urlpatterns = [
    path('user/register/', RegisterApi.as_view(), name="profile-register"),
    path('user/follow-profile/<str:username>', FollowApi.as_view(), name='follow'),
    path('user/is-follow-profile/<str:username>', IsFollowedApi.as_view(), name='is-follow'),
    path('user/verification/<str:username>/<str:token>', verify_email, name='verify-name'),


    # ================================================================================================


    path('user/profile/', UserProfileApi.as_view(), name="user-profile"),
    path('user/general/profile/<str:username>', GeneralProfileApi.as_view(), name="general-user-profile"),
    path('user/profile/followers/<str:username>', UserProfileFollowerListApi.as_view(), name="profile-followers"),
    path('user/profile/followings/<str:username>', UserProfileFollowingListApi.as_view(), name="profile-followings"),
    path('user/social-media/', UserProfileSocialMediaApi.as_view(), name="user-social-media"),
    path('user/social-media/<str:social_media_uuid>',
         UserProfileSocialMediaDetailApi.as_view(),
         name="user-social-media-detail"
         ),
    path('user/forget-password/', ForgetPasswordApi.as_view(), name='forget-password'),
    path('user/change-password/', ChangePasswordApi.as_view(), name='change-password'),


]
