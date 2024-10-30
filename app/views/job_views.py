from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Job, Application
from app.forms import JobForm, JobSearchForm
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def add_job(request):
    if request.user.user_type != "employer":
        return redirect("login")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("home")
    else:
        form = JobForm()
    return render(request, "app/job/add_job.html", {"form": form})


@login_required
def update_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user.employer)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("job_detail", job_id=job.id)
    else:
        form = JobForm(instance=job)

    return render(request, "app/job/update_job.html", {"form": form, "job": job})


@login_required
def job_detail(request, job_id):
    job = Job.objects.prefetch_related("programming_languages").get(id=job_id)
    num_applications = Application.objects.filter(job=job).count()
    context = {
        "job": job,
        "num_applications": num_applications,
    }
    if request.user.is_authenticated:
        if request.user.user_type == "employee":
            check_application = Application.objects.filter(
                employee=request.user.employee, job=job
            ).exists()

            if check_application:
                app = Application.objects.get(employee=request.user.employee, job=job)
                context["app"] = app
            context["check_application"] = check_application

    return render(request, "app/job/job_detail.html", context)


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        application = Application(employee=request.user.employee, job=job)
        application.save()
        return redirect("home")
    return render(request, "app/job/apply_job.html", {"job": job})


def job_search(request):
    form = JobSearchForm(request.GET or None)
    jobs = Job.objects.all()
    if form.is_valid():
        title = form.cleaned_data.get("title")
        if title:
            jobs = jobs.filter(title__icontains=title)

        company_name = form.cleaned_data.get("company_name")
        if company_name:
            jobs = jobs.filter(employer__company_name__icontains=company_name)

        city = form.cleaned_data.get("city")
        if city:
            jobs = jobs.filter(city=city)

        job_type = form.cleaned_data.get("job_type")
        if job_type:
            jobs = jobs.filter(job_types=job_type)

        experience_level = form.cleaned_data.get("experience_level")
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)

        programming_languages = form.cleaned_data.get("programming_languages")
        if programming_languages:
            jobs = jobs.filter(
                programming_languages__in=programming_languages
            ).distinct()

    return render(request, "app/job/job_search.html", {"form": form, "jobs": jobs})
