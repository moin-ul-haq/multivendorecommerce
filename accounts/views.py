from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from .forms import LoginForm, SignUpForm
from .tasks import send_login_email


def login_page(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        send_login_email.delay(user.email, user.name)
        return redirect("home")
    return render(request, "accounts/login.html", context={"form": form})


def signup_page(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "account created successfully")
        return redirect("home")
    return render(request, "accounts/signup.html", context={"form": form})


def logout_page(request):
    logout(request)
    return redirect("login_page")
