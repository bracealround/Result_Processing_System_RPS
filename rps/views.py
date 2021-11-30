from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login")
def home_view(request):

    return render(request, "home.html", {})


def students_view(request):
    return render(request, "students.html", {})


def teachers_view(request):
    return render(request, "teachers.html", {})


def results_view(request):
    return render(request, "results.html", {})


def edit_results_view(request):
    return render(request, "edit-results.html", {})
