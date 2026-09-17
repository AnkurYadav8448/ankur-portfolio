from django.shortcuts import render

from firebase.services import (
    get_projects,
    get_skills,
    get_profile,
)

from pages.models import Page
from experience.models import Experience
from certificates.models import Certificate


def home(request):
    # Firebase data
    projects = get_projects()
    skills = get_skills()
    profile = get_profile()

    # Keep these Django sections working for now
    navigation_pages = Page.objects.filter(
        published=True,
        show_in_navigation=True,
    ).order_by("title")

    experiences = Experience.objects.filter(
        published=True
    ).order_by("display_order", "-start_date")

    certificates = Certificate.objects.filter(
        published=True
    ).order_by("display_order", "-issue_date")

    # Firebase projects marked featured
    featured_projects = [
        project
        for project in projects
        if project.get("featured") is True
    ][:3]

    context = {
        "projects": projects,
        "featured_projects": featured_projects,
        "skills": skills,
        "profile": profile,
        "navigation_pages": navigation_pages,
        "experiences": experiences,
        "certificates": certificates,
    }

    return render(
        request,
        "home.html",
        context,
    )