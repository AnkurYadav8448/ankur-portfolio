from django.contrib import admin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path

from firebase.services import (
    delete_firebase_message,
    get_firebase_messages,
    mark_firebase_message_read,
)

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

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "firebase-messages/",
                self.admin_site.admin_view(
                    self.firebase_messages_view
                ),
                name="firebase_messages",
            ),
            path(
                "firebase-messages/<str:message_id>/read/",
                self.admin_site.admin_view(
                    self.firebase_message_read
                ),
                name="firebase_message_read",
            ),
            path(
                "firebase-messages/<str:message_id>/delete/",
                self.admin_site.admin_view(
                    self.firebase_message_delete
                ),
                name="firebase_message_delete",
            ),
        ]

        return custom_urls + urls

    def firebase_messages_view(self, request):
        messages_data = get_firebase_messages()

        context = {
            **self.admin_site.each_context(request),
            "title": "Firebase Messages",
            "messages_data": messages_data,
        }

        return TemplateResponse(
            request,
            "admin/firebase_messages.html",
            context,
        )

    def firebase_message_read(self, request, message_id):
        mark_firebase_message_read(message_id)

        return redirect(
            "admin:firebase_messages"
        )

    def firebase_message_delete(self, request, message_id):
        if request.method == "POST":
            delete_firebase_message(message_id)

        return redirect(
            "admin:firebase_messages"
        )