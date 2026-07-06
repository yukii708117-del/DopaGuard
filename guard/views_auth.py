from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from guard.forms_auth import SignupForm


def home(request):
    return render(request, "guard/home.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "会員登録が完了しました。")
            return redirect("home")
    else:
        form = SignupForm()

    return render(request, "guard/signup.html", {"form": form})


class GuardLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class GuardLogoutView(LogoutView):
    pass