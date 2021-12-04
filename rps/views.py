from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from decimal import Decimal
from logging import *
from rps.models import Course, Department, Mark, Student, Teacher
from .forms import individual_resultForm, upload_csv_form


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
    return render(request, "dashboard.html", {"courses": list(query_set)})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def students_view(request):
    student = Student.objects.get(user=request.user)
    return render(request, "students.html", {"student": student})


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def teachers_view(request):
    teacher = Teacher.objects.get(user=request.user)
    return render(request, "teachers.html", {"teacher": teacher})


def department_view(request):
    dept = Department.objects.all()
    return render(request, "department.html", {"department": list(dept)})


def institute_teacher_view(request):
    teacher = Teacher.objects.all()
    return render(request, "institute_teachers.html", {"ins_teacher": list(teacher)})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def results_view(request):

    query_set = Mark.objects.filter(student__user=request.user)

    return render(request, "results.html", {"marks": list(query_set)})


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def edit_results_view(request):
    teacher = Teacher.objects.get(user=request.user)
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = individual_resultForm(request.POST, teacher=teacher)
        csv_form = upload_csv_form(request.POST, teacher=teacher)
        # check whether it's valid:
        if form.is_valid():
            print(form)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            return redirect("edit-results")

        elif csv_form.is_valid():
            print("csv: ", request.FILES["csv_file"])
            return redirect("edit-results")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = individual_resultForm(teacher=teacher)
        csv_form = upload_csv_form(teacher=teacher)

    return render(request, "edit-results.html", {"form": form, "csv_form": csv_form})


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "csv_upload.html", data)
        # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "File is not CSV type")
            return HttpResponseRedirect(reverse("csv_upload"))
            # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(
                request,
                "Uploaded file is too big (%.2f MB)."
                % (csv_file.size / (1000 * 1000),),
            )
            return HttpResponseRedirect(reverse("csv_upload"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        print("debug")
        for line in lines:
            fields = line.split(",")
            mark = Mark()
            registration_no = int(fields[0])
            print(1)
            student = Student.objects.get(registration_no=registration_no)
            print(2)
            mark.student = student
            print(3)
            course = Course.objects.get(course_code="BNG101")
            print(4)
            mark.course = course
            mark.term_test = Decimal(fields[1])
            print(5)
            mark.attendance = int(fields[2])
            print(6)
            mark.total_attendence = int(fields[3])
            print(7)
            mark.other_assesment = Decimal(fields[4])
            print(8)
            mark.semester_final = Decimal(fields[5])
            print(9)
            mark.save()

        # loop over the lines and save them in db. If error , store as string and then display
        # for line in lines:
        # 	fields = line.split(",")
        # 	data_dict = {}
        # 	data_dict["name"] = fields[0]
        # 	data_dict["start_date_time"] = fields[1]
        # 	data_dict["end_date_time"] = fields[2]
        # 	data_dict["notes"] = fields[3]
        # 	try:
        # 		form = EventsForm(data_dict)
        # 		if form.is_valid():
        # 			form.save()
        # 		else:
        # 			logging.getLogger("error_logger").error(form.errors.as_json())
        # 	except Exception as e:
        # 		logging.getLogger("error_logger").error(repr(e))
        # 		pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("csv_upload"))
