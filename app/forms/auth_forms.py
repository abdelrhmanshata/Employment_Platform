from django import forms
from django.contrib.auth import get_user_model
from app.models import Employee, Employer, City, ProgrammingLanguage
from django.core.validators import RegexValidator

User = get_user_model()


class EmployeeRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )
    #
    national_id = forms.CharField(
        min_length=14,
        max_length=14,
        required=True,
        validators=[
            RegexValidator(r"^\d{14}$", "National ID must be exactly 14 digits.")
        ],
        help_text="Please enter your 14-digit National ID",
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), required=False, label="City"
    )
    new_city = forms.CharField(
        max_length=100,
        required=False,
        help_text="Add new city if not listed",
        label="New City",
    )
    experience_level = forms.ChoiceField(choices=Employee.Experience_CHOICES)
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
    biography = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Employee
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            #
            "national_id",
            "city",
            "new_city",
            "experience_level",
            "programming_languages",
            "new_programming_languages",
            "biography",
        ]

    def clean(self):
        cleaned_data = super().clean()
        self._validate_password(cleaned_data)
        self._validate_city(cleaned_data)
        self._validate_programming_languages(cleaned_data)
        return cleaned_data

    def _validate_password(self, cleaned_data):
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

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

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            user_type="employee",
        )
        employee = super().save(commit=False)
        employee.user = user

        employee.city = self._get_or_create_city()

        if commit:
            employee.save()
            self.save_m2m()
            self._add_new_programming_languages(employee)
        return employee

    def _get_or_create_city(self):
        new_city = self.cleaned_data.get("new_city")
        if new_city:
            city_obj, created = City.objects.get_or_create(name=new_city)
            return city_obj
        return self.cleaned_data["city"]

    def _add_new_programming_languages(self, employee):
        new_languages = self.cleaned_data.get("new_programming_languages")
        if new_languages:
            new_languages_list = [
                lang.strip() for lang in new_languages.split(",") if lang.strip()
            ]
            for language in new_languages_list:
                lang_obj, created = ProgrammingLanguage.objects.get_or_create(
                    name=language
                )
                employee.programming_languages.add(lang_obj)


class EmployeeProfileForm(forms.ModelForm):
    national_id = forms.CharField(
        min_length=14,
        max_length=14,
        required=True,
        validators=[
            RegexValidator(r"^\d{14}$", "National ID must be exactly 14 digits.")
        ],
        help_text="Please enter your 14-digit National ID",
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), required=False, label="City"
    )
    new_city = forms.CharField(
        max_length=100,
        required=False,
        help_text="Add new city if not listed",
        label="New City",
    )

    experience_level = forms.ChoiceField(choices=Employee.Experience_CHOICES)
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
    biography = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Employee
        fields = [
            "national_id",
            "city",
            "new_city",
            "experience_level",
            "programming_languages",
            "new_programming_languages",
            "biography",
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

    def save(self, commit=True):
        employee = super().save(commit=False)
        employee.city = self._get_or_create_city()
        if commit:
            employee.save()
            self.save_m2m()
            self._add_new_programming_languages(employee)
        return employee

    def _get_or_create_city(self):
        new_city = self.cleaned_data.get("new_city")
        if new_city:
            city_obj, created = City.objects.get_or_create(name=new_city)
            return city_obj
        return self.cleaned_data["city"]

    def _add_new_programming_languages(self, employee):
        new_languages = self.cleaned_data.get("new_programming_languages")
        if new_languages:
            new_languages_list = [
                lang.strip() for lang in new_languages.split(",") if lang.strip()
            ]
            for language in new_languages_list:
                lang_obj, created = ProgrammingLanguage.objects.get_or_create(
                    name=language
                )
                employee.programming_languages.add(lang_obj)


################################################################################################


class EmployerRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )
    #
    company_name = forms.CharField(max_length=255)
    company_description = forms.Textarea()
    logo = forms.ImageField(required=False)

    class Meta:
        model = Employer
        fields = (
            "username",
            "email",
            "password",
            "confirm_password",
            #
            "company_name",
            "company_description",
            "logo",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
            email=self.cleaned_data["email"],
            user_type="employer",
        )

        employer = super().save(commit=False)
        employer.user = user

        if "logo" in self.cleaned_data and self.cleaned_data["logo"]:
            employer.logo = self.cleaned_data["logo"]

        if commit:
            employer.save()
        return employer


class EmployerProfilerForm(forms.ModelForm):
    company_name = forms.CharField(max_length=255)
    company_description = forms.Textarea()
    logo = forms.ImageField(required=False)

    class Meta:
        model = Employer
        fields = ("company_name", "company_description", "logo")

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        employer = super().save(commit=False)

        if "logo" in self.cleaned_data and self.cleaned_data["logo"]:
            employer.logo = self.cleaned_data["logo"]

        if commit:
            employer.save()
        return employer
