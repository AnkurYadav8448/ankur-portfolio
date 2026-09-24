from django.db import models


class Project(models.Model):

    # =========================================================
    # BASIC PROJECT INFORMATION
    # =========================================================

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True
    )

    short_description = models.CharField(
        max_length=300
    )

    description = models.TextField()


    # =========================================================
    # PROJECT IMAGE
    # =========================================================

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True
    )


    # =========================================================
    # TECHNOLOGIES
    # =========================================================

    technologies = models.CharField(
        max_length=500,
        help_text="Example: Python, Django, Excel, SQL, Power BI"
    )


    # =========================================================
    # PROJECT LINKS
    # =========================================================

    github_url = models.URLField(
        blank=True,
        null=True
    )

    live_url = models.URLField(
        blank=True,
        null=True
    )


    # =========================================================
    # DISPLAY SETTINGS
    # =========================================================

    featured = models.BooleanField(
        default=False
    )

    published = models.BooleanField(
        default=True
    )


    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    # =========================================================
    # META
    # =========================================================

    class Meta:
        ordering = ["-created_at"]


    # =========================================================
    # STRING REPRESENTATION
    # =========================================================

    def __str__(self):
        return self.title