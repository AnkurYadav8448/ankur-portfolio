from django.contrib import admin

from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "published",
        "show_in_navigation",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "published",
        "show_in_navigation",
        "created_at",
    )

    search_fields = (
        "title",
        "slug",
        "short_description",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    ordering = ("-created_at",)