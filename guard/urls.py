from django.urls import path

from guard import views_auth

urlpatterns = [
    path("", views_auth.home, name="home"),
    path("signup/", views_auth.signup, name="signup"),
    path("accounts/login/", views_auth.GuardLoginView.as_view(), name="login"),
    path("accounts/logout/", views_auth.GuardLogoutView.as_view(), name="logout"),
]