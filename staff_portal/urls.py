from django.urls import path

from . import views

app_name = "staff_portal"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("manager/", views.manager, name="manager"),
    path("register/", views.register, name="register"),
    path("verify/<path:token>/", views.verify_email, name="verify_email"),
]
