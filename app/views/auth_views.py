from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from app.forms import (
    EmployeeRegisterForm,
    EmployerRegisterForm,

)
from app.auth_backend import EmailAuthBackend
from django.contrib.auth import get_user_model

User = get_user_model()

def user_register_employee(request):
    if request.method == "POST":
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EmployeeRegisterForm()
    return render(request, "auth/register_employee.html", {"form": form})


def user_register_employer(request):
    if request.method == "POST":
        form = EmployerRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = EmployerRegisterForm()
    return render(request, "auth/register_employer.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = EmailAuthBackend.authenticate(
            None, request, username=email, password=password
        )
        if user is not None:
            user.backend = "app.auth_backend.EmailAuthBackend"
            login(request, user)
            if user.user_type == "employee":
                return redirect("employee_dashboard")
            elif user.user_type == "employer":
                return redirect("employer_dashboard")
        else:
            return render(
                request, "auth/login.html", {"error": "Invalid email or password"}
            )

    return render(request, "auth/login.html")


def user_logout(request):
    logout(request)
    return redirect("home")
