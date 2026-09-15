from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    # =========================================================
    # LIST PAGE
    # =========================================================

    list_display = (
        "title",
        "featured",
        "published",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "featured",
        "published",
        "created_at",
    )

    search_fields = (
        "title",
        "short_description",
        "description",
        "technologies",
    )

    ordering = (
        "-created_at",
    )


    # =========================================================
    # SLUG
    # =========================================================

    prepopulated_fields = {
        "slug": (
            "title",
        )
    }


    # =========================================================
    # EDIT PAGE
    # =========================================================

    fieldsets = (
        (
            "Project Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "short_description",
                    "description",
                )
            },
        ),

        (
            "Project Image",
            {
                "fields": (
                    "image",
                )
            },
        ),

        (
            "Technologies",
            {
                "fields": (
                    "technologies",
                )
            },
        ),

        (
            "Project Links",
            {
                "fields": (
                    "github_url",
                    "live_url",
                )
            },
        ),

        (
            "Publication",
            {
                "fields": (
                    "featured",
                    "published",
                )
            },
        ),
    )