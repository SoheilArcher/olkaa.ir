from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("en/", views.home, {"lang": "en"}, name="home_en"),
    path("ar/", views.home, {"lang": "ar"}, name="home_ar"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap"),
]
