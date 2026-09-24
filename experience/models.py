from django.db import models


class Experience(models.Model):
    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    job_title = models.CharField(
        max_length=200,
    )

    company = models.CharField(
        max_length=200,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )


    # =========================================================
    # DATES
    # =========================================================

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="Leave blank if this is your current position.",
    )

    currently_working = models.BooleanField(
        default=False,
        help_text="Check this if this is your current position.",
    )


    # =========================================================
    # DESCRIPTION
    # =========================================================

    description = models.TextField(
        blank=True,
    )

    responsibilities = models.TextField(
        blank=True,
        help_text="Describe your main responsibilities and work.",
    )

    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Example: Python, Excel, SQL, Power BI, Django",
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
    )


    # =========================================================
    # TIMESTAMP
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
            "-start_date",
        ]
        verbose_name = "Experience"
        verbose_name_plural = "Experience"


    # =========================================================
    # STRING
    # =========================================================

    def __str__(self):
        return f"{self.job_title} — {self.company}"