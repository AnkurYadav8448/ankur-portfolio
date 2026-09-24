from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import home
from pages.views import resume


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Home
    path("", home, name="home"),

    # Contact
    path("contact/", include("contact.urls")),

    # Projects
    path("projects/", include("projects.urls")),

    # Pages
    path("pages/", include("pages.urls")),

    # Resume
    path("resume/", resume, name="resume"),
]


# Serve uploaded media files during local development.
# Vercel/production does not use Django's local media server.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )