from .auth_views import (
    user_register_employee,
    user_register_employer,
    user_login,
    user_logout,
)

from .employee_views import (
    employee_dashboard,
    employee_profile,
    employee_applied_jobs,
    employee_details,
)

from .employer_views import (
    employer_dashboard,
    employer_profile,
    manage_applications,
    accept_application,
    reject_application,
)

from .job_views import add_job, job_detail, update_job, apply_job, job_search

from .views import home, user_profile
