from django.db import models


class Profile(models.Model):
    # =========================================================
    # BASIC PROFILE
    # =========================================================

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


    # =========================================================
    # ABOUT SECTION
    # =========================================================

    about_data_analytics = models.TextField(
        blank=True,
        default=(
            "Data cleaning, analysis, Excel, SQL, "
            "dashboards, reporting and visualization."
        ),
        help_text="Description for the Data Analytics card.",
    )

    about_python = models.TextField(
        blank=True,
        default=(
            "Python, Django, automation, "
            "database-driven applications and "
            "practical software solutions."
        ),
        help_text="Description for the Python Development card.",
    )

    about_problem_solving = models.TextField(
        blank=True,
        default=(
            "I focus on creating practical, useful "
            "solutions for real business and data problems."
        ),
        help_text="Description for the Problem Solving card.",
    )


    # =========================================================
    # FILES
    # =========================================================

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


    # =========================================================
    # CONTACT INFORMATION
    # =========================================================

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


    # =========================================================
    # STATUS
    # =========================================================

    website_status = models.BooleanField(
        default=True,
        help_text="Enable or disable the public profile.",
    )


    # =========================================================
    # TIMESTAMP
    # =========================================================

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    # =========================================================
    # META
    # =========================================================

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


    # =========================================================
    # STRING
    # =========================================================

    def __str__(self):
        return self.name