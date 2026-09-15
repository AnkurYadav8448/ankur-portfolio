from django.db import models


class Certificate(models.Model):
    # =========================================================
    # BASIC INFORMATION
    # =========================================================

    title = models.CharField(
        max_length=200,
    )

    issuer = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )


    # =========================================================
    # CERTIFICATE DETAILS
    # =========================================================

    issue_date = models.DateField(
        blank=True,
        null=True,
    )

    credential_id = models.CharField(
        max_length=200,
        blank=True,
    )

    credential_url = models.URLField(
        blank=True,
    )


    # =========================================================
    # FILE / IMAGE
    # =========================================================

    certificate_file = models.FileField(
        upload_to="certificates/",
        blank=True,
        null=True,
        help_text="Upload the certificate PDF or image.",
    )


    # =========================================================
    # DISPLAY SETTINGS
    # =========================================================

    display_order = models.PositiveIntegerField(
        default=0,
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
            "-issue_date",
        ]
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"


    # =========================================================
    # STRING
    # =========================================================

    def __str__(self):
        return f"{self.title} — {self.issuer}"