from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "professional_title",
        "email",
        "website_status",
        "updated_at",
    )

    search_fields = (
        "name",
        "professional_title",
        "email",
        "location",
    )

    list_filter = (
        "website_status",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    def has_add_permission(self, request):
        """
        Allow only one Profile record.
        """
        if Profile.objects.exists():
            return False

        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting the main profile accidentally.
        """
        return False