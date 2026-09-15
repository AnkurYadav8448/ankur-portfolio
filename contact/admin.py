from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "read",
        "created_at",
    )

    list_filter = (
        "read",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Visitor Information",
            {
                "fields": (
                    "name",
                    "email",
                ),
            },
        ),
        (
            "Message",
            {
                "fields": (
                    "subject",
                    "message",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "read",
                    "created_at",
                ),
            },
        ),
    )