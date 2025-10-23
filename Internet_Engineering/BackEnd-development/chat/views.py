from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render
from jwt import decode as jwt_decode
from django.conf import settings

from chat.models import ChatRoom_Member, ChatRoom
from profiles.models import Profile
from users.models import BaseUser


# Create your views here.



def chatbox_view(request, username, jwt):
    decoded_data = jwt_decode(jwt, settings.SECRET_KEY, algorithms=["HS256"])
    user1 = BaseUser.objects.get(id=decoded_data["user_id"])
    user2 = Profile.objects.get(username=username).user


    temp = ChatRoom.objects.filter(chatroom_member__member__in=[user1, user2]).values('id').annotate(
        count=Count("chat_room_id")).filter(count=2).values('id').first()

    if temp is None:
        ChatRoom.objects.create_direct_chat(user1, user2)
        print("No Chatroom exists for these two users")

    print(jwt)
    # return HttpResponse(f"Your token is : {jwt}")
    return render(request, 'chatbox/index.html', {"user_email": user1.email, 'jwt': jwt})
