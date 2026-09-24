from django.contrib import messages
from django.shortcuts import redirect, render

from firebase.services import get_profile, save_message

from .forms import ContactMessageForm


def submit_contact(request):
    profile = get_profile()

    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            save_message(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["message"],
            )

            messages.success(
                request,
                "Your message has been sent successfully. Thank you!",
            )

            return redirect("contact")

        messages.error(
            request,
            "Please check the form and try again.",
        )

    else:
        form = ContactMessageForm()

    return render(
        request,
        "contact.html",
        {
            "form": form,
            "profile": profile,
        },
    )