from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import home
from pages.views import resume


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", home, name="home"),

    path("contact/", include("contact.urls")),

    path("projects/", include("projects.urls")),

    path("pages/", include("pages.urls")),

    path("resume/", resume, name="resume"),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )