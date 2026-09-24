from django.db import models


class Profile(models.Model):
    name = models.CharField(
        max_length=150,
        default="Ankur Yadav",
    )

    professional_title = models.CharField(
        max_length=200,
        default="Data Analytics & Python Developer",
    )

    short_intro = models.CharField(
        max_length=300,
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    profile_photo = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
    )

    resume = models.FileField(
        upload_to="resume/",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    linkedin_url = models.URLField(
        blank=True,
    )

    github_url = models.URLField(
        blank=True,
    )

    instagram_url = models.URLField(
        blank=True,
    )

    website_status = models.BooleanField(
        default=True,
        help_text="Enable or disable the public profile.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.name