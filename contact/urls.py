from django.urls import path

from .views import submit_contact


urlpatterns = [
    path("", submit_contact, name="contact"),
    path("submit/", submit_contact, name="submit_contact"),
]