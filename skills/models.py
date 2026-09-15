from django.db import models


class Skill(models.Model):

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    name = models.CharField(
        max_length=100,
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: Programming, Data Analytics, Database",
    )


    # =========================================================
    # SKILL LEVEL
    # =========================================================

    level = models.PositiveIntegerField(
        default=80,
        help_text="Skill level from 0 to 100.",
    )


    # =========================================================
    # OPTIONAL ICON
    # =========================================================

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon name or CSS class.",
    )


    # =========================================================
    # DESCRIPTION
    # =========================================================

    description = models.CharField(
        max_length=300,
        blank=True,
    )


    # =========================================================
    # DISPLAY SETTINGS
    # =========================================================

    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first.",
    )

    published = models.BooleanField(
        default=True,
        help_text="Show this skill on the public portfolio.",
    )


    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    # =========================================================
    # META
    # =========================================================

    class Meta:

        ordering = [
            "display_order",
            "name",
        ]

        verbose_name = "Skill"
        verbose_name_plural = "Skills"


    # =========================================================
    # STRING REPRESENTATION
    # =========================================================

    def __str__(self):
        return self.name