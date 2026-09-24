from django.shortcuts import get_object_or_404, render

from .models import Project


def project_list(request):
    projects = Project.objects.filter(
        published=True
    ).order_by("-created_at")

    return render(
        request,
        "project_list.html",
        {
            "projects": projects,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(
        Project,
        slug=slug,
        published=True,
    )

    return render(
        request,
        "project_detail.html",
        {
            "project": project,
        },
    )