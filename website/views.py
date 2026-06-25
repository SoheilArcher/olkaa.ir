from django.shortcuts import render


def home(request):
    """صفحه‌ی فرود معرفی شرکت."""
    return render(request, "website/home.html")
