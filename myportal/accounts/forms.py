from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["display_name", "company", "notes"]
        widgets = {
            "display_name": forms.TextInput(attrs={"id": "id_display_name"}),
            "company": forms.TextInput(attrs={"id": "id_company"}),
            "notes": forms.Textarea(attrs={"id": "id_notes", "rows": 4}),
        }