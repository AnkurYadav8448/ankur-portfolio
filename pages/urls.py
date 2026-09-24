from django.urls import path

from .views import page_detail, resume


urlpatterns = [
    path("resume/", resume, name="resume"),
    path("<slug:slug>/", page_detail, name="page_detail"),
]