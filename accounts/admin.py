from django.contrib import admin
from .models import Profile


# ==========================================================
#                       PROFILE ADMIN
# ==========================================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "user",

        "image",

    )

    search_fields = (

        "user__username",

        "user__first_name",

        "user__last_name",

        "user__email",

    )

    ordering = (

        "user__username",

    )