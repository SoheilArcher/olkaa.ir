from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("portal/", include("staff_portal.urls")),
    path("", include("website.urls")),
]
