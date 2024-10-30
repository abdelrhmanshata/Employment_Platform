from django.db.models import Q
from app.models import Employee
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from employment_platform.settings import DEFAULT_FROM_EMAIL


def notify_employee_of_acceptance(application):
    subject = "Job Application Status"
    context = {
        "employee_name": application.employee.user.username,
        "job_title": application.job.title,
        "company_name": application.job.employer.company_name,
    }
    html_message = render_to_string("emails/acceptance.html", context)
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [application.employee.user.email]
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
    )


def notify_employee_of_rejection(application):
    subject = "Job Application Status"
    context = {
        "employee_name": application.employee.user.username,
        "job_title": application.job.title,
        "company_name": application.job.employer.company_name,
    }
    html_message = render_to_string("emails/rejection.html", context)
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [application.employee.user.email]
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
    )


def notify_matching_employees(job):
    matching_employees = Employee.objects.filter(
        Q(programming_languages__in=job.programming_languages.all())
        | Q(experience_level=job.experience_level)
    ).distinct()

    if matching_employees:
        biography_texts = [employee.biography for employee in matching_employees]
        job_description = job.description

        documents = biography_texts + [job_description]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)

        resume_matrix = tfidf_matrix[:-1]
        job_matrix = tfidf_matrix[-1:]

        similarities = cosine_similarity(resume_matrix, job_matrix)

        results = []
        for i, employee in enumerate(matching_employees):
            results.append(
                {
                    "employee": employee,
                    "similarity": similarities[i][0],
                }
            )
        results = sorted(results, key=lambda x: x["similarity"], reverse=True)

        threshold = 0.1
        for result in results:
            print("result",result["similarity"])
            if result["similarity"] > threshold:
                send_job_notification_email(result["employee"], job)


def send_job_notification_email(employee, job):
    subject = f"New Job Opportunity: {job.title}"
    context = {"employee_name": employee.user.username, "job": job}
    html_message = render_to_string("emails/notify_job_creation.html", context)
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [employee.user.email]
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
    )
