from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == "employer":
            return redirect("employer_dashboard")
    return redirect("employee_dashboard")


##################################################################################################


@login_required
def user_profile(request):
    if request.user.is_authenticated:
        if request.user.user_type == "employer":
            return redirect("employer_profile")
        elif request.user.user_type == "employee":
            return redirect("employee_profile")
    return redirect("login")
