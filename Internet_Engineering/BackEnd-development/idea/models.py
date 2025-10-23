import os
import uuid
from django.db import models, IntegrityError, transaction
import time
from django.utils import timezone

from profiles.models import Profile
from users.models import BaseUser


# Create your models here.


def idea_upload_image_path(instance, filename):
    """Save idea images in PROJECT_ROOT/media/idea_pics/ directory"""
    ext = filename.split('.')[-1]
    return os.path.join(
        "idea_pics",
        f'{str(instance.uuid)}_{int(round(time.time() * 1000))}.{ext}'
    )


def idea_upload_attachment_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(
        "idea_attachments",
        str(instance.idea.uuid),
        f'{str(instance.uuid)}_{int(round(time.time() * 1000))}.{ext}'
    )


class Classification(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Idea(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    classification = models.ManyToManyField(Classification)
    title = models.CharField(max_length=100)
    goal = models.CharField(max_length=500)
    abstract = models.CharField(max_length=1500)
    description = models.TextField()
    image = models.ImageField(upload_to=idea_upload_image_path, null=True, blank=True)

    attached_files_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    max_donation = models.PositiveIntegerField(default=0)
    total_donation = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    show_likes = models.BooleanField(default=True)
    show_views = models.BooleanField(default=True)
    show_comments = models.BooleanField(default=True)

    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class IdeaAttachmentFile(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    idea = models.ForeignKey(to=Idea, on_delete=models.CASCADE)
    file = models.FileField(upload_to=idea_upload_attachment_path)
    created_at = models.DateTimeField(default=timezone.now)


class SavedIdea(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "idea")


class IdeaReport(models.Model):
    REASON_TYPES = ["Spam", "Promoting Violence", "Encouragement to commit suicide"]
    __REASON_CHOICES = [(i.lower(), i) for i in REASON_TYPES]

    idea = models.ForeignKey(to=Idea, on_delete=models.CASCADE, related_name="reported_idea")
    reporter = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="reporter_idea")
    report_reasons = models.CharField(choices=__REASON_CHOICES, max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)



# ==================================================================================================


class IdeaComment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    idea = models.ForeignKey(to=Idea, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)


class IdeaLikes(models.Model):
    date = models.DateField(auto_now_add=True)
    profile_id = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    idea_id = models.ForeignKey(to=Idea, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile_id', 'idea_id')


class FinancialStep(models.Model):
    FINANCIAL_UNIT_TYPES = ['rial', 'dollar', 'euro']
    __FINANCIAL_UNIT_CHOICES = [(x, x.lower()) for x in FINANCIAL_UNIT_TYPES]

    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    unit = models.CharField(max_length=20, choices=__FINANCIAL_UNIT_CHOICES)
    priority = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('idea', 'priority')



class ProfileReport(models.Model):
    REASON_TYPES = ["Spam", "Promoting Violence", "Encouragement to commit suicide"]

    __REASON_CHOICES = [(i.lower(), i) for i in REASON_TYPES]
    date = models.DateTimeField(auto_now_add=True)
    profile_id = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="reported_profile")
    reporter_id = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="reporter_profile")
    report_reasons = models.CharField(choices=__REASON_CHOICES, max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    is_checked = models.BooleanField(default=False)



class CollaborationRequest(models.Model):
    COLLABORATION_STATUS_TYPES = ['full_time', 'part_time', 'other']

    __COLLABORATION_STATUS_CHOICES = [(x, x) for x in COLLABORATION_STATUS_TYPES]

    title = models.CharField(max_length=200, blank=True, null=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    skills = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=__COLLABORATION_STATUS_CHOICES, blank=True, null=True)
    education = models.CharField(max_length=200)
    description = models.TextField()
    salary = models.PositiveIntegerField()




class IdeaViewManager(models.Manager):
    def create(self, user: BaseUser, idea: Idea):
        try:
            with transaction.atomic():
                instance = super().create(user=user, idea=idea)
        except IntegrityError:
            pass

        else:
            idea.views_count += 1
            idea.save()
            return instance



class IdeaViews(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = IdeaViewManager()

    class Meta:
        unique_together = ('user', 'idea')


