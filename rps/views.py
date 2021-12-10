from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction, IntegrityError
from django.db.models import Count, Sum, Value
from django.db.models.functions import Concat
from decimal import Decimal
import logging
from rps import models
from rps.models import Course, Department, Mark, Staffs, Student, Teacher
from .forms import individual_resultForm, upload_csv_form, edit_profile
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import html_to_pdf #created in step 4
import datetime
from django.template.loader import render_to_string

#Creating a class based view
class GeneratePdf_view(View):
     def get(self, request, *args, **kwargs):
        data = Mark.objects.all()
        open('temps.html', "w").write(render_to_string('results.html', {'data': data}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temps.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')



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

    if request.user.is_teacher:
        first_name = Teacher.objects.get(user=request.user).first_name
        last_name = Teacher.objects.get(user=request.user).last_name
        full_name = first_name + " " + last_name

    elif request.user.is_student:
        first_name = Student.objects.get(user=request.user).first_name
        last_name = Student.objects.get(user=request.user).last_name
        full_name = first_name + " " + last_name

    else:
        full_name = "Admin"

    total_number_dept = Department.objects.all().count()
    total_number_student = Student.objects.all().count()
    total_number_teacher = Teacher.objects.all().count()
    total_number_staff = Staffs.objects.all().count()
    return render(request, "dashboard.html", {"name": full_name, "total_number_of_dept": total_number_dept, "total_number_of_students":total_number_student, 
    "total_number_of_teachers": total_number_teacher, "total_number_of_staffs": total_number_staff})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def students_view(request):
    # student = Student.objects.get(user=request.user)
    student = Student.objects.get(user=request.user)
    return render(request, "students.html", {"student": student})

@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def enrollment_view(request):
    # student = Student.objects.get(user=request.user)
    course = Course.objects.all()
    return render(request, "enrollment.html", {"course": course})

@login_required(login_url="login")
def staff_view(request):
    staff = Staffs.objects.all()
    return render(request, "staffs.html", {"staff": list(staff)})


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def teachers_view(request):
    teacher = Teacher.objects.get(user=request.user)
    return render(request, "teachers.html", {"teacher": teacher})


@login_required(login_url="login")
def department_view(request):
    query_set = Department.objects.annotate(
        number_of_teachers=Count("teacher", distinct=True)
    ).annotate(number_of_students=Count("student", distinct=True))
    return render(request, "department.html", {"departments": list(query_set)})

@login_required(login_url="login")
def institute_students_view(request):
    student = Student.objects.all()
    return render(request, "institute_students.html", {"ins_student": list(student)})


@login_required(login_url="login")
def institute_teacher_view(request):
    teacher = Teacher.objects.all()
    return render(request, "institute_teachers.html", {"ins_teacher": list(teacher)})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def edit_students_profile_view(request):
    student = Student.objects.get(user=request.user)

    if request.method == "POST":
        form = edit_profile(
            request.POST, first_name=student.first_name, last_name=student.last_name
        )

        try:
            with transaction.atomic():
                if form.is_valid():
                    print("yep")

                    first_name = form.cleaned_data["first_name"]
                    last_name = form.cleaned_data["last_name"]

                    student.first_name = first_name
                    student.last_name = last_name

                    student.save()

                    request.session["is_saved"] = "True"

        except IntegrityError as e:
            request.session["error"] = str(e)
        except Exception as e:
            request.session["error"] = str(e)

    else:
        form = edit_profile(first_name=student.first_name, last_name=student.last_name)

    render_response = render(
        request, "edit_students_profile.html", {"student": student, "form": form}
    )

    request.session.pop("error", None)
    request.session.pop("is_saved", None)
    return render_response


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def edit_teachers_profile_view(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == "POST":
        form = edit_profile(
            request.POST, first_name=teacher.first_name, last_name=teacher.last_name
        )

        try:
            with transaction.atomic():
                if form.is_valid():
                    print("yep")

                    first_name = form.cleaned_data["first_name"]
                    last_name = form.cleaned_data["last_name"]

                    teacher.first_name = first_name
                    teacher.last_name = last_name

                    teacher.save()

                    request.session["is_saved"] = "True"

        except IntegrityError as e:
            request.session["error"] = str(e)
        except Exception as e:
            request.session["error"] = str(e)

    else:
        form = edit_profile(first_name=teacher.first_name, last_name=teacher.last_name)

    render_response = render(
        request, "edit_teachers_profile.html", {"teacher": teacher, "form": form}
    )

    request.session.pop("error", None)
    request.session.pop("is_saved", None)
    return render_response


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def results_view(request):

    query_set = Mark.objects.filter(student__user=request.user)
    total_credits = query_set.aggregate(Sum("course__credit_no"))[
        "course__credit_no__sum"
    ]
    print("total: ", total_credits)
    marks = list(query_set)

    sum = Decimal("0.0")
    for mark in marks:
        sum = sum + (mark.gpa * mark.course.credit_no)

    print(sum)
    cgpa = sum / total_credits
    print("cgpa: ", cgpa)
    return render(
        request, "results.html", {"marks": list(query_set), "cgpa": round(cgpa, 2), "completed_credit": round(total_credits,2)}
    )


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def view_results_view(request):

    query_set = Mark.objects.filter(course__teacher__user=request.user)

    return render(request, "view-results.html", {"marks": list(query_set)})


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def edit_results_view(request):

    teacher = Teacher.objects.get(user=request.user)
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # request.session.pop("error", None)
        # create a form instance and populate it with data from the request:
        form = individual_resultForm(request.POST, teacher=teacher)
        csv_form = upload_csv_form(request.POST, teacher=teacher)
        # check whether it's valid:
        if form.is_valid():

            csv_form = upload_csv_form(teacher=teacher)
            # print(form)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            try:
                with transaction.atomic():
                    mark = Mark()

                    registration_no = form.cleaned_data["registration_no"]
                    student = Student.objects.get(registration_no=registration_no)
                    mark.student = student

                    mark.course = form.cleaned_data["course"]
                    mark.term_test = form.cleaned_data["term_test"]
                    mark.attendance = form.cleaned_data["attendance"]
                    mark.total_attendence = form.cleaned_data["total_attendence"]
                    mark.other_assesment = form.cleaned_data["other_assesment"]
                    mark.semester_final = form.cleaned_data["semester_final"]

                    mark.save()

            except ValueError as e:
                request.session[
                    "error"
                ] = "Some field contains data of unexpected type."

            except IntegrityError as e:
                request.session["error"] = "Record probably already exists."

            except Exception as e:
                request.session["error"] = str(e)

            # return redirect("edit-results")

        elif csv_form.is_valid():

            form = individual_resultForm(teacher=teacher)
            # print("csv: ", request.FILES["csv_file"])

            try:
                upload_csv(request, csv_form.cleaned_data["course"])

            except IntegrityError as e:
                # print("gubbbbbb ", str(e))
                request.session["error"] = str(e)

            except Exception as e:
                # print("gub ", str(e))
                request.session["error"] = str(e)

            # return redirect("edit-results")

    # if a GET (or any other method) we'll create a blank form
    else:
        request.session.pop("error", None)
        form = individual_resultForm(teacher=teacher)
        csv_form = upload_csv_form(teacher=teacher)

    render_response = render(
        request, "edit-results.html", {"form": form, "csv_form": csv_form}
    )
    request.session.pop("error", None)
    return render_response


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def upload_csv(request, course):
    # data = {}
    # if "GET" == request.method:
    #     return render(request, "csv_upload.html", data)
    #     # if not GET, then proceed
    try:
        with transaction.atomic():
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith(".csv"):
                raise TypeError(
                    "It was probably not a CSV file. Please upload a CSV file"
                )
                # messages.error(request, "File is not CSV type")
                # return HttpResponseRedirect(reverse("csv_upload"))
                # if file is too large, return
            if csv_file.multiple_chunks():
                raise Exception(
                    "Uploaded file is too big (%.2f MB)."
                    % (csv_file.size / (1000 * 1000),)
                )
                # messages.error(
                #     request,
                #     "Uploaded file is too big (%.2f MB)."
                #     % (csv_file.size / (1000 * 1000),),
                # )
                # return HttpResponseRedirect(reverse("csv_upload"))

            file_data = csv_file.read().decode("utf-8")

            lines = file_data.split("\n")
            # print("debug")

            index = 0
            try:
                for index, line in enumerate(lines):
                    fields = line.split(",")
                    mark = Mark()
                    registration_no = int(fields[0])
                    print(index)
                    student = Student.objects.get(registration_no=registration_no)
                    # print(2)
                    mark.student = student
                    # print(3)
                    # print(4)
                    mark.course = course
                    mark.term_test = Decimal(fields[1])
                    # print(5)
                    mark.attendance = int(fields[2])
                    # print(6)
                    mark.total_attendence = int(fields[3])
                    # print(7)
                    mark.other_assesment = Decimal(fields[4])
                    # print(8)
                    mark.semester_final = Decimal(fields[5])
                    # print(9)
                    mark.save()
            except ValueError as e:
                raise ValueError(
                    "CSV contains data of unexpected type at record no. "
                    + str(index + 1)
                    + "."
                )

            except IntegrityError as e:
                raise IntegrityError(
                    "CSV may be containing duplicate record at row "
                    + str(index + 1)
                    + "."
                )

            except Exception as e:
                print(repr(e))
                raise Exception(
                    "CSV contains invalid data. Please fix it and try again. Hint: Check record no. "
                    + str(index + 1)
                    + "."
                )

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
    except TypeError as e:
        raise TypeError(str(e))

    except ValueError as e:
        raise ValueError(str(e))

    except IntegrityError as e:
        raise IntegrityError(str(e))

    except Exception as e:
        raise Exception(str(e))
        # logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        # messages.error(request, "Unable to upload file. " + repr(e))
    # return HttpResponseRedirect(reverse("csv_upload"))
