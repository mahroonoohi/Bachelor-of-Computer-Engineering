from django.contrib import admin

from idea.models import Idea, IdeaAttachmentFile, SavedIdea, IdeaReport, IdeaComment, IdeaLikes, FinancialStep, \
    ProfileReport, Classification

# Register your models here.


admin.site.register(Idea)
admin.site.register(IdeaAttachmentFile)
admin.site.register(SavedIdea)
admin.site.register(IdeaReport)
admin.site.register(IdeaComment)
admin.site.register(IdeaLikes)
admin.site.register(FinancialStep)
admin.site.register(ProfileReport)
admin.site.register(Classification)

