from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from rps.models import Course, Mark


# Function for checking whether user is a student or not
def is_student(user):
    if user:
        return user.is_student

    return False


# Function for checking whether user is a teacher or not
def is_teacher(user):
    if user:
        return user.is_teacher

    return False


# Create your views here.
@login_required(login_url="login")
def home_view(request):
    query_set = Course.objects.all()
    return render(request, "home.html", {"courses": list(query_set)})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def students_view(request):
    return render(request, "students.html", {})


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def teachers_view(request):
    return render(request, "teachers.html", {})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def results_view(request):

    query_set = Mark.objects.filter(student__user=request.user)

    return render(request, "results.html", {"marks": list(query_set)})


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def edit_results_view(request):
    return render(request, "edit-results.html", {})
