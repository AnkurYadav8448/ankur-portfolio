from django.contrib import messages
from django.shortcuts import redirect

from .forms import ContactMessageForm


def submit_contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your message has been sent successfully. Thank you!"
            )
        else:
            messages.error(
                request,
                "Please check the form and try again."
            )

    return redirect("home")