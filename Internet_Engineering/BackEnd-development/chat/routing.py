from django.urls import path
from . import consumers

websocket_urlpatterns = [

    path('ws/chat/chatroom/<str:room_name>/', consumers.ChatRoomConsumer.as_asgi()),
    path('ws/chat/userchats/', consumers.UserChats.as_asgi()),

    # ==============================================================================================

    path('ws/user/info/', consumers.UserInfo.as_asgi()),
    path('ws/media/<str:room_name>/', consumers.SendMedia.as_asgi()),
    path('ws/delete/<str:room_name>/', consumers.DeleteMessage.as_asgi()),
]
