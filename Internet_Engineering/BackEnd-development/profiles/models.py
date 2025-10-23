import os

from django.db import models
import uuid
from users.models import BaseUser
import time


# Create your models here.


def profile_upload_image_path(instance, filename):
    """Save profile image in PROJECT_ROOT/media/profile_pics/INSTANCE_ID directory"""
    ext = filename.split('.')[-1]
    return os.path.join(
        "profile_pics",
        str(instance.username),
        f'{str(instance.username)}_{int(round(time.time() * 1000))}.{ext}'
    )



class Address(models.Model):
    country = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)



class Profile(models.Model):

    GENDER_TYPES = ['male', 'female', 'other']

    __GENDER_CHOICES = [(i, i) for i in GENDER_TYPES]

    gender = models.CharField(max_length=15, choices=__GENDER_CHOICES, default='other')
    birth_date = models.DateField(null=True, blank=True)

    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, unique=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)

    bio = models.CharField(max_length=512, null=True, blank=True)
    profile_image = models.ImageField(upload_to=profile_upload_image_path, null=True, blank=True)

    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    idea_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    max_donation = models.PositiveIntegerField(default=0)  # required donation
    total_donation = models.PositiveIntegerField(default=0)  # total donation amount

    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    show_likes = models.BooleanField(default=True)
    show_views = models.BooleanField(default=True)
    show_comments = models.BooleanField(default=True)

    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} >> {self.username}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Follow(models.Model):
    date = models.DateField(auto_now_add=True)
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_follower_set')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_following_set')

    class Meta:
        unique_together = ('follower', 'following')


class ProfileLinks(models.Model):

    LINK_TYPES = ['github', 'gitlab', 'telegram', 'linkedin', 'instagram', 'facebook', 'twitter']
    __LINK_TYPE_CHOICES = [(i, i) for i in LINK_TYPES]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=__LINK_TYPE_CHOICES)
    link = models.URLField(max_length=500)

    class Meta:
        unique_together = ('profile', 'type')

