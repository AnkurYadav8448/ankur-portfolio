from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = (
            "name",
            "email",
            "subject",
            "message",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Your Name",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Your Email",
                    "autocomplete": "email",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "placeholder": "Subject",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Write your message...",
                    "rows": 6,
                }
            ),
        }