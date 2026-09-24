from django.contrib import admin

from .models import Experience


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "company",
        "location",
        "start_date",
        "end_date",
        "currently_working",
        "published",
    )

    search_fields = (
        "job_title",
        "company",
        "location",
        "technologies",
        "description",
    )

    list_filter = (
        "currently_working",
        "published",
    )

    ordering = (
        "display_order",
        "-start_date",
    )