from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _

UserAdmin.fieldsets = (
    (None, {"fields": ("username", "email", "password")}),
    (_("Personal info"), {"fields": ("first_name", "last_name", "home_address")}),
    (
        _("Permissions"),
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
    ),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
)

UserAdmin.add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "home_address"),
        },
    ),
)

admin.site.register(CustomUser, UserAdmin)