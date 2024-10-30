from django import forms
from django.contrib.auth import get_user_model
from app.models import City, ProgrammingLanguage, Job, Application, Employer

User = get_user_model()


class ApplicationSearchForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        label="City",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    experience_level = forms.ChoiceField(
        choices=[("", "All")] + list(Job.Experience_CHOICES),
        required=False,
        label="Experience Level",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    programming_languages = forms.ModelMultipleChoiceField(
        queryset=ProgrammingLanguage.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
        label="Programming Languages",
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Search bio text", "rows": 4}
        ),
        label="Bio Text",
    )
    job_type = forms.ChoiceField(
        choices=[("", "All")] + list(Job.Job_Types),
        required=False,
        label="Job Type",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Application
        fields = []
