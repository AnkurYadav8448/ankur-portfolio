from django.shortcuts import render

from pages.models import Page
from projects.models import Project
from skills.models import Skill
from userprofile.models import Profile
from experience.models import Experience
from certificates.models import Certificate

from contact.forms import ContactMessageForm


def home(request):
    projects = Project.objects.filter(
        published=True
    ).order_by("-created_at")

    featured_projects = projects.filter(
        featured=True
    )[:3]

    navigation_pages = Page.objects.filter(
        published=True,
        show_in_navigation=True,
    ).order_by("title")

    skills = Skill.objects.filter(
        published=True
    ).order_by("display_order", "name")

    profile = Profile.objects.filter(
        website_status=True
    ).first()

    experiences = Experience.objects.filter(
        published=True
    ).order_by("display_order", "-start_date")

    certificates = Certificate.objects.filter(
        published=True
    ).order_by("display_order", "-issue_date")

    contact_form = ContactMessageForm()

    context = {
        "projects": projects,
        "featured_projects": featured_projects,
        "navigation_pages": navigation_pages,
        "skills": skills,
        "profile": profile,
        "experiences": experiences,
        "certificates": certificates,
        "contact_form": contact_form,
    }

    return render(request, "home.html", context)