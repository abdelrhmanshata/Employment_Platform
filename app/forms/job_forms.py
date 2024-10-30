from django import forms
from django.contrib.auth import get_user_model
from app.models import City, ProgrammingLanguage, Job, Application

User = get_user_model()


class JobForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), required=False, label="City"
    )
    new_city = forms.CharField(
        max_length=100,
        required=False,
        help_text="Add new city if not listed",
        label="New City",
    )
    experience_level = forms.ChoiceField(choices=Job.Experience_CHOICES)
    job_types = forms.ChoiceField(choices=Job.Job_Types)
    programming_languages = forms.ModelMultipleChoiceField(
        queryset=ProgrammingLanguage.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        label="Programming Languages",
    )
    new_programming_languages = forms.CharField(
        max_length=255,
        required=False,
        help_text="Add new languages if not listed (separate by commas)",
        label="New Programming Languages",
    )

    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "city",
            "new_city",
            "experience_level",
            "job_types",
            "programming_languages",
            "new_programming_languages",
        ]

    def clean(self):
        cleaned_data = super().clean()
        self._validate_city(cleaned_data)
        self._validate_programming_languages(cleaned_data)
        return cleaned_data

    def _validate_city(self, cleaned_data):
        city = cleaned_data.get("city")
        new_city = cleaned_data.get("new_city")
        if not city and not new_city:
            raise forms.ValidationError("Please select a city or add a new one.")

    def _validate_programming_languages(self, cleaned_data):
        programming_languages = cleaned_data.get("programming_languages")
        new_programming_languages = cleaned_data.get("new_programming_languages")
        if not programming_languages and not new_programming_languages:
            raise forms.ValidationError(
                "Please select a Programming Language or add a new one."
            )

    def save(self, commit=True, user=None):
        job = super().save(commit=False)
        job.employer = user.employer

        job.city = self._get_or_create_city()

        if commit:
            job.save()
            self.save_m2m()
            self._add_new_programming_languages(job)
        return job

    def _get_or_create_city(self):
        new_city = self.cleaned_data.get("new_city")
        if new_city:
            city_obj, created = City.objects.get_or_create(name=new_city)
            return city_obj
        return self.cleaned_data["city"]

    def _add_new_programming_languages(self, job):
        new_languages = self.cleaned_data.get("new_programming_languages")
        if new_languages:
            new_languages_list = [
                lang.strip() for lang in new_languages.split(",") if lang.strip()
            ]
            for language in new_languages_list:
                lang_obj, created = ProgrammingLanguage.objects.get_or_create(
                    name=language
                )
                job.programming_languages.add(lang_obj)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = []


class JobSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="Job Title",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    company_name = forms.CharField(
        max_length=255,
        required=False,
        label="Company Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        label="City",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    job_type = forms.ChoiceField(
        choices=[("", "All")] + list(Job.Job_Types),
        required=False,
        label="Job Type",
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

    class Meta:
        model = Job
        fields = []
