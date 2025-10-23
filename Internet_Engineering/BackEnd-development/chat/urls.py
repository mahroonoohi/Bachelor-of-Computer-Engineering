from django.urls import path
from .views import chatbox_view

urlpatterns = [
    path('chatpage/<str:username>/<str:jwt>', chatbox_view, name='chat_page'),
]
