from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Job, Application
from app.forms import EmployerProfilerForm, ApplicationSearchForm
from django.contrib.auth import get_user_model
from app.utils import mail

User = get_user_model()


@login_required
def employer_dashboard(request):
    if request.user.user_type != "employer":
        return redirect("login")
    
    employer = request.user.employer
    jobs = Job.objects.filter(employer=employer)
    return render(request, "app/employer/employer_dashboard.html", {"jobs": jobs})


@login_required
def employer_profile(request):
    if request.user.user_type != "employer":
        return redirect("login")

    if request.method == "POST":
        form = EmployerProfilerForm(
            request.POST, request.FILES, instance=request.user.employer
        )
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EmployerProfilerForm(instance=request.user.employer)

    return render(
        request,
        "app/employer/employer_profile.html",
        {"form": form, "employer": request.user.employer},
    )


@login_required
def manage_applications(request):
    if request.user.user_type != "employer":
        return redirect("login")

    employer = request.user.employer
    employer_jobs = Job.objects.filter(employer=employer)
    applications = Application.objects.filter(job__in=employer_jobs)

    form = ApplicationSearchForm(request.GET or None)
    if form.is_valid():
        city = form.cleaned_data.get("city")
        if city:
            applications = applications.filter(employee__city=city)

        experience_level = form.cleaned_data.get("experience_level")
        if experience_level:
            applications = applications.filter(
                employee__experience_level=experience_level
            )

        job_type = form.cleaned_data.get("job_type")
        if job_type:
            applications = applications.filter(job__job_types=job_type)

        bio = form.cleaned_data.get("bio")
        if bio:
            applications = applications.filter(employee__biography__icontains=bio)

        programming_languages = form.cleaned_data.get("programming_languages")
        if programming_languages:
            applications = applications.filter(
                employee__programming_languages__in=programming_languages
            ).distinct()

    context = {
        "applications": applications,
        "form": form,
    }
    return render(request, "app/employer/manage_applications.html", context)


def accept_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = "Accepted"
    application.save()
    mail.notify_employee_of_acceptance(application)
    return redirect("manage_applications")


def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = "Rejected"
    application.save()
    mail.notify_employee_of_rejection(application)
    return redirect("manage_applications")
