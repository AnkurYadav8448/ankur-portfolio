from django.contrib import admin

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    # =========================================================
    # LIST DISPLAY
    # =========================================================

    list_display = (
        "name",
        "category",
        "level",
        "display_order",
        "published",
        "created_at",
        "updated_at",
    )


    # =========================================================
    # FILTERS
    # =========================================================

    list_filter = (
        "category",
        "published",
    )


    # =========================================================
    # SEARCH
    # =========================================================

    search_fields = (
        "name",
        "category",
        "description",
    )


    # =========================================================
    # DEFAULT ORDER
    # =========================================================

    ordering = (
        "display_order",
        "name",
    )


    # =========================================================
    # EDIT FORM
    # =========================================================

    fieldsets = (
        (
            "Skill Information",
            {
                "fields": (
                    "name",
                    "category",
                    "description",
                )
            },
        ),

        (
            "Skill Level",
            {
                "fields": (
                    "level",
                ),
                "description": "Enter a value from 0 to 100.",
            },
        ),

        (
            "Icon",
            {
                "fields": (
                    "icon",
                )
            },
        ),

        (
            "Display Settings",
            {
                "fields": (
                    "display_order",
                    "published",
                )
            },
        ),
    )