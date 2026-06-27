from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import StaffLoginForm

app_name = "staff_portal"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            authentication_form=StaffLoginForm,
            extra_context={"portal_login": True},
            next_page="/portal/",
            redirect_authenticated_user=True,
            template_name="staff_portal/login.html",
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("otp/", views.email_otp, name="email_otp"),
    path("shifts/", views.shifts, name="shifts"),
    path("finance/", views.finance, name="finance"),
    path("live/", views.live, name="live"),
    path("manager/", views.manager, name="manager"),
    path("register/", views.register, name="register"),
    path("verify/<path:token>/", views.verify_email, name="verify_email"),
]
