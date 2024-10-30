from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Job, Application, Employee, ProfileView
from app.forms import EmployeeProfileForm
from django.contrib.auth import get_user_model
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from django.db.models import Q

User = get_user_model()


def employee_dashboard(request):
    jobs = Job.objects.all()

    context = {"jobs": jobs}
    #
    if request.user.is_authenticated:
        if request.user.user_type == "employee":
            employee = request.user.employee
            matching_jobs = Job.objects.filter(
                Q(programming_languages__in=employee.programming_languages.all())
                | Q(experience_level=employee.experience_level)
            ).distinct()

        if matching_jobs.exists():
            description_texts = [job.description for job in matching_jobs]
            employee_biography = employee.biography

            documents = description_texts + [employee_biography]

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(documents)

            resume_matrix = tfidf_matrix[:-1]
            job_matrix = tfidf_matrix[-1:]

            similarities = cosine_similarity(resume_matrix, job_matrix)

            results = []
            for i, job in enumerate(matching_jobs):
                results.append(
                    {
                        "job": job,
                        "similarity": similarities[i][0],
                    }
                )
            results = sorted(results, key=lambda x: x["similarity"], reverse=True)

            threshold = 0.5
            jobMatching = [
                result for result in results if result["similarity"] > threshold
            ]
            context["jobMatching"] = jobMatching
    return render(request, "app/employee/employee_dashboard.html", context)


@login_required
def employee_profile(request):
    if request.user.user_type != "employee":
        return redirect("login")

    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, instance=request.user.employee)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EmployeeProfileForm(instance=request.user.employee)

    count = ProfileView.objects.filter(employee=request.user.employee).count()
    return render(
        request,
        "app/employee/employee_profile.html",
        {"form": form, "employee": request.user.employee, "count": count},
    )


@login_required
def employee_applied_jobs(request):
    if request.user.user_type != "employee":
        return redirect("login")
    application_jobs = Application.objects.filter(employee=request.user.employee)
    return render(
        request,
        "app/employee/employee_applied_jobs.html",
        {"application_jobs": application_jobs},
    )


@login_required
def employee_details(request, employee_id):
    if request.user.user_type != "employer":
        return redirect("login")

    employee = get_object_or_404(Employee, id=employee_id)
    employer = request.user.employer

    profileView, created = ProfileView.objects.get_or_create(
        employee=employee, employer=employer
    )

    count = ProfileView.objects.filter(employee=employee).count()
    context = {"employee": employee, "count": count}
    return render(request, "app/employee/employee_details.html", context)
