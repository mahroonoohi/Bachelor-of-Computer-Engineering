from django.contrib import admin
from profiles.models import Profile, ProfileLinks, Follow

# Register your models here.


admin.site.register(Profile)
admin.site.register(ProfileLinks)
admin.site.register(Follow)
