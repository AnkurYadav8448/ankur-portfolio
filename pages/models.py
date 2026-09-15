from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        help_text="Example: about-me or data-analytics",
    )

    short_description = models.CharField(
        max_length=300,
        blank=True,
    )

    content = models.TextField()

    featured_image = models.ImageField(
        upload_to="pages/",
        blank=True,
        null=True,
    )

    published = models.BooleanField(default=True)

    show_in_navigation = models.BooleanField(
        default=False,
        help_text="Show this page in the main navigation.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title