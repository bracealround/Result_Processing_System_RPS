from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_teacher",
        "is_student",
    )

    search_fields = ("email",)
    readonly_fields = ("date_joined", "last_login")

    ordering = ("email",)
    filter_horizontal = ()
    list_filter = ()

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "date_joined",
                    "is_staff",
                    "is_teacher",
                    "is_student",
                )
            },
        ),
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "date_joined",
                    "is_staff",
                    "is_teacher",
                    "is_student",
                )
            },
        ),
    )


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
