from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from users.models import BaseUser


# Register your models here.





class BaseUserAdmin(UserAdmin):
    readonly_fields = ('updated_at', 'created_at')
    list_editable = ['is_email_verified']
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("created_at", "updated_at", "is_email_verified")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    # add_form = BaseUserCreationForm

    ordering = ("email",)
    list_display = ("email", "is_admin", "is_email_verified")
    list_filter = ("is_admin", "is_superuser", "is_active", "groups")


admin.site.register(BaseUser, BaseUserAdmin)
