from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import (
    CustomUser,
    Employer,
    Employee,
    City,
    Job,
    Application,
    ProgrammingLanguage,
    ProfileView,
)


admin.site.register(CustomUser)
admin.site.register(Employer)
admin.site.register(Employee)
admin.site.register(City)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(ProgrammingLanguage)
admin.site.register(ProfileView)
