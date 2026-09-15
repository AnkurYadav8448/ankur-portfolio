from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "issuer",
        "issue_date",
        "credential_id",
        "published",
        "display_order",
    )

    search_fields = (
        "title",
        "issuer",
        "credential_id",
        "description",
    )

    list_filter = (
        "published",
        "issue_date",
    )

    ordering = (
        "display_order",
        "-issue_date",
    )