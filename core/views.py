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
    """
    Homepage view.

    Firebase data is loaded safely so that a temporary
    Firebase/API problem does not crash the complete homepage.
    """

    # ---------------------------------------------------------
    # Default values
    # ---------------------------------------------------------

    projects = []
    skills = []
    profile = {}

    navigation_pages = []
    experiences = []
    certificates = []

    # ---------------------------------------------------------
    # Firebase data
    # ---------------------------------------------------------

    try:
        projects = get_projects() or []
    except Exception:
        projects = []

    try:
        skills = get_skills() or []
    except Exception:
        skills = []

    try:
        profile = get_profile() or {}
    except Exception:
        profile = {}

    # ---------------------------------------------------------
    # Django database data
    # ---------------------------------------------------------

    try:
        navigation_pages = (
            Page.objects
            .filter(
                published=True,
                show_in_navigation=True,
            )
            .order_by("title")
        )
    except Exception:
        navigation_pages = []

    try:
        experiences = (
            Experience.objects
            .filter(
                published=True
            )
            .order_by(
                "display_order",
                "-start_date",
            )
        )
    except Exception:
        experiences = []

    try:
        certificates = (
            Certificate.objects
            .filter(
                published=True
            )
            .order_by(
                "display_order",
                "-issue_date",
            )
        )
    except Exception:
        certificates = []

    # ---------------------------------------------------------
    # Featured projects
    # ---------------------------------------------------------

    featured_projects = [
        project
        for project in projects
        if isinstance(project, dict)
        and project.get("featured") is True
    ][:3]

    # ---------------------------------------------------------
    # Template context
    # ---------------------------------------------------------

    context = {
        "projects": projects,
        "featured_projects": featured_projects,
        "skills": skills,
        "profile": profile,
        "navigation_pages": navigation_pages,
        "experiences": experiences,
        "certificates": certificates,
    }

    # ---------------------------------------------------------
    # Render homepage
    # ---------------------------------------------------------

    return render(
        request,
        "home.html",
        context,
    )