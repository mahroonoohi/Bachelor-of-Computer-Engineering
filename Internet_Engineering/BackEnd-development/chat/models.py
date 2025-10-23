from django.db import models
from django.utils.crypto import get_random_string
import base64
from django.core.files import File
import time
import os
from django.db.models import Count
from django.conf import settings

from chat.exceptions import ChatRoomExistsError
from users.models import BaseUser

# Create your models here.


class ChatroomManager(models.Manager):
    def create(self):
        chat_room_id = get_random_string(50)
        while super().get_queryset().filter(chat_room_id=chat_room_id).exists():
            chat_room_id = get_random_string(50)

        instance = self.model(chat_room_id=chat_room_id)
        instance.save()
        return instance

    def create_direct_chat(self, member1: BaseUser, member2: BaseUser):
        temp = ChatRoom_Member.objects.filter(
            member__in=[member1, member2]
        ).values('chat_room').annotate(count=Count('chat_room')).filter(count=2)

        if temp.exists():
            raise ChatRoomExistsError("A direct chat exists for these users")

        instance = self.create()
        ChatRoom_Member.objects.create(chat_room=instance, member=member1)
        ChatRoom_Member.objects.create(chat_room=instance, member=member2)
        return instance


class ChatRoom(models.Model):

    chat_room_id = models.CharField(max_length=50, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = ChatroomManager()

    def __str__(self):
        return self.chat_room_id



class ChatRoom_Member(models.Model):

    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    member = models.ForeignKey(BaseUser, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('chat_room', 'member')

    def __str__(self):
        return self.chat_room.chat_room_id


def image_message_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(
        "image_messages", str(instance.sender.id), str(
            instance.chat_room.id), f'{round(time.time() * 1000)}.{ext}'
    )


def file_message_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(
        "file_messages", str(instance.sender.id), str(
            instance.chat_room.id), f'{round(time.time() * 1000)}.{ext}'
    )


class MessageManager(models.Manager):

    def __create_media_message(self, sender, chat_room, base64_file_data: str, file_extension: str):
        instance = self.model(sender=sender, chat_room=chat_room)
        base64_bytes = base64_file_data.encode('utf-8')
        temp_file_path = os.path.join(
            settings.BASE_DIR, 'temp', f'{sender.id}-{round(time.time() * 1000)}.{file_extension}')
        with open(temp_file_path, 'wb') as file:
            file.write(base64.decodebytes(base64_bytes))

        return instance, temp_file_path

    def create_image_message(self, sender, chat_room, image_base64_data: str, file_extension: str):
        instance, temp_file_path = self.__create_media_message(
            sender, chat_room, image_base64_data, file_extension)
        instance.type = 'image'
        instance.text = None
        instance.voice = None
        with open(temp_file_path, 'rb') as file:
            instance.image = File(file)
            instance.save()
        print(temp_file_path)
        os.remove(temp_file_path)
        return instance

    def create_voice_message(self, sender, chat_room, voice_base64_data: str, file_extension: str):
        instance, temp_file_path = self.__create_media_message(
            sender, chat_room, voice_base64_data, file_extension)
        instance.type = 'voice'
        instance.text = None
        instance.image = None
        with open(temp_file_path, 'rb') as file:
            instance.voice = File(file)
            instance.save()
        os.remove(temp_file_path)
        return instance

    def create_text_message(self, sender, chat_room, text):
        instance = self.model(sender=sender, chat_room=chat_room,
                              text=text, type='text', voice=None, image=None)
        instance.save()
        return instance


class Message(models.Model):
    MESSAGE_TYPES = ['text', 'image', 'voice']

    __message_choices = [(x, x) for x in MESSAGE_TYPES]
    type = models.CharField(max_length=10, choices=__message_choices, default='text')
    sender = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

    text = models.TextField(null=True)
    image = models.ImageField(upload_to=image_message_path, null=True)
    voice = models.FileField(upload_to=file_message_path, null=True)

    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    send_date = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return self.chat_room.chat_room_id


