from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    #
    path("register/employee/", views.user_register_employee, name="register_employee"),
    path("register/employer/", views.user_register_employer, name="register_employer"),
    #
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    #
    path("profile/", views.user_profile, name="profile"),
    path("employee/", views.employee_dashboard, name="employee_dashboard"),
    path("employer/", views.employer_dashboard, name="employer_dashboard"),
    path("employee/profile", views.employee_profile, name="employee_profile"),
    path("employer/profile", views.employer_profile, name="employer_profile"),
    #
    path(
        "employee/<int:employee_id>/", views.employee_details, name="employee_details"
    ),
    #
    path("job/add/", views.add_job, name="add_job"),
    path("job/<int:job_id>/", views.job_detail, name="job_detail"),
    path("job/update/<int:job_id>/", views.update_job, name="update_job"),
    path("job/apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("job/search/", views.job_search, name="job_search"),
    #
    path("job/applied/", views.employee_applied_jobs, name="applied_jobs"),
    #
    path("manage_applications/", views.manage_applications, name="manage_applications"),
    path(
        "accept/<int:application_id>/",
        views.accept_application,
        name="accept_application",
    ),
    path(
        "reject/<int:application_id>/",
        views.reject_application,
        name="reject_application",
    ),
]
