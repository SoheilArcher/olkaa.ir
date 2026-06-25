from django.urls import path

from . import views

app_name = "staff_portal"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("otp/", views.email_otp, name="email_otp"),
    path("finance/", views.finance, name="finance"),
    path("live/", views.live, name="live"),
    path("manager/", views.manager, name="manager"),
    path("register/", views.register, name="register"),
    path("verify/<path:token>/", views.verify_email, name="verify_email"),
]
