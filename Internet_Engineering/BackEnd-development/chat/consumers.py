import base64
import json
import os
import pathlib
import time
import traceback
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q
from django.core.files import File
from django.conf import settings
from channels.layers import get_channel_layer
from channels import DEFAULT_CHANNEL_LAYER

from .serializer import serialize_message
from .models import ChatRoom, Message, ChatRoom_Member
from users.models import BaseUser
from profiles.models import Profile


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']

        temp = ChatRoom_Member.objects.filter(
            chat_room__chat_room_id=self.room_name, member=self.user)

        if temp:
            self.chatroom = temp.first().chat_room
            self.room_group_name = f'direct_{self.room_name}'
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            print("Accepted...")
            self.accept()

            messages = Message.objects.filter(chat_room=self.chatroom).order_by('send_date')
            message_list = {'event': 'message', 'messages': [
                serialize_message(m) for m in messages]}
            self.send(text_data=json.dumps(message_list))

        else:
            print("Rejected...")
            self.close()

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name)
        except AttributeError:
            pass
        self.close()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['message_type']

        if message_type not in Message.MESSAGE_TYPES:
            self.send(text_data=json.dumps(
                {'event': 'error', 'description': 'Bad message type !'}))

        else:
            if message_type == 'text':
                message = Message.objects.create_text_message(
                    self.user, self.chatroom, text_data_json['text'])

            elif message_type == 'image':
                # data = text_data_json['data'].split(';base64,')[1]
                data = text_data_json['data']
                message = Message.objects.create_image_message(
                    self.user,
                    self.chatroom, data,
                    text_data_json['file_extension']
                )
            else:
                # data = text_data_json['data'].split(';base64,')[1]
                data = text_data_json['data']
                message = Message.objects.create_voice_message(
                    self.user,
                    self.chatroom, data,
                    text_data_json['file_extension']
                )


            message = serialize_message(message)
            context = {
                'type': 'chatroom_message',
                'message': message,
            }
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, context)

    def chatroom_message(self, event):
        # message = event['message']
        #
        # messages = serialize_message(message)
        messages = event['message']
        data = {
            'event': "message",
            'messages': [messages]
        }

        text_data = json.dumps(data)
        self.send(text_data=text_data)

    def delete_message(self, event):
        message_id = event['message_id']
        data = {'event': "delete_message", 'message_id': message_id}

        text_data = json.dumps(data)
        self.send(text_data=text_data)


class UserChats(WebsocketConsumer):

    @staticmethod
    def update_chat_list(user, user_roles=None):
        ch_layer = get_channel_layer(DEFAULT_CHANNEL_LAYER)
        context = {
            'type': 'user_chat_list',
            'event': 'chat_list_all' if not user_roles else 'chat_list_slice',
            'chats': UserChats.user_chat_rooms(user, user_roles)
        }
        async_to_sync(ch_layer.group_send)(UserChats.get_channel_group_name(user), context)

    @staticmethod
    def get_channel_group_name(user):
        return f'user_chats_{user.email}'.replace('@', '..')

    @staticmethod
    def user_chat_rooms(user, roles=None):

        directs = ChatRoom_Member.objects.filter(
            member=user,
        ).select_related('chat_room')

        chatrooms = list()

        for i in directs:
            data = {
                'chatroom_id': i.chat_room.chat_room_id,
                'chatroom_type': 'direct',
                'chatroom_title': ChatRoom_Member.objects.filter(
                    Q(chat_room=i.chat_room) & ~Q(member=i.member)
                ).select_related('member').first().member.email,
                'user_role': 'member'
            }
            chatrooms.append(data)

        return chatrooms

    def connect(self):
        self.user = self.scope['user']
        if not self.user:
            self.close()

        else:
            self.accept()
            print(f"XXXXXXXXXXXXXXX: {UserChats.get_channel_group_name(self.user)}")
            async_to_sync(self.channel_layer.group_add)(
                UserChats.get_channel_group_name(self.user), self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        roles = json_data.get('roles', None)

        context = {
            'type': 'user_chat_list',
            'event': 'chat_list_all' if not roles else 'chat_list_slice',
            'chats': UserChats.user_chat_rooms(self.user, roles)
        }
        async_to_sync(self.channel_layer.group_send)(UserChats.get_channel_group_name(self.user), context)

    def user_chat_list(self, event):
        chats = event['chats']
        ev = event['event']
        data = {
            'event': ev,
            'chats': chats
        }
        text_data = json.dumps(data)
        self.send(text_data=text_data)

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name)
        except AttributeError:
            pass
        self.close()


# ======================================================================================


class SendMedia(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        temp = ChatRoom_Member.objects.filter(chat_room__chat_room_id=self.room_name, member=self.user)
        if temp:
            self.chatroom = temp.first().chat_room
            self.accept()

    def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        message_id = json_data['message_id']
        messages = Message.objects.filter(chat_room__chat_room_id=self.room_name, id=message_id)
        if messages.exists() and messages.first().type in ['voice', 'image']:
            message = messages.first()
            if message.type == 'voice':
                file = message.voice
            else:
                file = message.image

            file_data = file.read()

            base64_bytes = base64.b64encode(file_data)
            base64_string = base64_bytes.decode('utf-8')
            data = {'event': 'file_contents',
                    'message_id': message.id,
                    'file_name': pathlib.PurePath(file.path).name,
                    'data': base64_string
                    }

            self.send(text_data=json.dumps(data))
        else:
            self.send(text_data=json.dumps({'event': 'error', 'description': "Invalid message id"}))


class DeleteMessage(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']

        temp = ChatRoom_Member.objects.filter(chat_room__chat_room_id=self.room_name, member=self.user)

        if temp.exists():

            self.chatroom = temp.first().chat_room
            self.room_group_name = f'direct_{self.room_name}'

            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            print("Accepted...")
            self.accept()

        else:
            print("Rejected...")
            self.close()

    def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        message_id = json_data['message_id']
        messages = Message.objects.filter(chat_room=self.chatroom, sender=self.user, id=message_id)

        if messages.exists():
            message = messages.first()
            message.delete()
            context = {
                'type': 'delete_message',
                'message_id': message_id,
            }
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, context)

        else:
            data = {'event': 'error', 'description': 'No message found with this id !'}
            self.send(text_data=json.dumps(data))

    def delete_message(self, event):
        message_id = event['message_id']
        data = {'event': "delete_message", 'message_id': message_id}

        text_data = json.dumps(data)
        self.send(text_data=text_data)

    def chatroom_message(self, event):
        # message = event['message']
        #
        # messages = serialize_message(message)
        messages = event['message']
        data = {
            'event': "message",
            'messages': [messages]
        }

        text_data = json.dumps(data)
        self.send(text_data=text_data)


class UserInfo(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']

        if not self.user:
            self.close()
        else:
            self.accept()

    def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        user_email = json_data['user_email']
        profile = Profile.objects.filter(user__email=user_email)

        if profile.exists():
            profile = profile.first()
            profile_pic = None
            profile_pic_name = None
            if profile.profile_image:
                pic = profile.profile_image.read()
                base64_bytes = base64.b64encode(pic)
                profile_pic = base64_bytes.decode('utf-8')
                profile_pic_name = pathlib.PurePath(profile.profile_image.path).name

            data = {
                'event': 'user_info',
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'phone_number': "10203040",
                'email': profile.user.email,
                'profile_pic': profile_pic,
                'profile_pic_name': profile_pic_name
            }

            self.send(text_data=json.dumps(data))
        else:
            self.send(text_data=json.dumps({'event': 'error', 'description': 'Bad user email'}))
