from django.db.models import BooleanField
from django.db.models.expressions import Exists, OuterRef, Case, Subquery, When, Q
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
import logging, datetime
import os
from rps import models
from rps.models import (
    Course,
    Department,
    Mark,
    Staff,
    Student,
    Teacher,
    Enrollment,
    Assignment,
    pdfupload,
)
from .forms import individual_resultForm, upload_csv_form, edit_profile, select_semester
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import html_to_pdf  # created in step 4
import datetime
from django.template.loader import render_to_string

# Creating a class based view
class GeneratePdf_view(View):
    def get(self, request, *args, **kwargs):
        # data = Mark.objects.all().order_by("enrollment__course__course")
        # data = {"data": "dummy_data"}
        # print("tets", d)
        # open("tmp.html", "w").write(
        #     render_to_string("rps/results.html", {"data": data})
        # )

        query_set = Mark.objects.filter(
            enrollment__student__user=request.user, is_approved=True
        )
        if query_set.exists():
            total_credits = query_set.aggregate(
                Sum("enrollment__course__course__credit_no")
            )["enrollment__course__course__credit_no__sum"]
            print("total: ", total_credits)
            marks = list(query_set)

            sum = Decimal("0.0")
            for mark in marks:
                sum = sum + (mark.gpa * mark.enrollment.course.course.credit_no)

            print(sum)
            cgpa = sum / total_credits
            print("cgpa: ", cgpa)
        else:
            cgpa = Decimal("0.0")
            total_credits = Decimal("0.0")

        registration_no = Student.objects.get(user=request.user).registration_no
        department = Student.objects.get(user=request.user).department
        session = Student.objects.get(user=request.user).session
        total_credits_earned =Mark.objects.filter(
        enrollment__student__user=request.user, is_approved=True
        ).aggregate(
            Sum("enrollment__course__course__credit_no")
        )["enrollment__course__course__credit_no__sum"]

        d = {
            "data": list(query_set),
            "cgpa": cgpa,
            "registration_no": registration_no,
            "department": department,
            "session": session,
            "total_credits_earned": total_credits_earned,
        }
        # d = {str(index): str(value) for index, value in enumerate(list(query_set))}

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf("rps/pdfresult.html", d)

        # rendering the template
        return HttpResponse(pdf, content_type="application/pdf")


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

    if request.user.is_teacher and Teacher.objects.filter(user=request.user).exists():
        first_name = Teacher.objects.get(user=request.user).first_name
        last_name = Teacher.objects.get(user=request.user).last_name
        full_name = first_name + " " + last_name

    elif request.user.is_student and Student.objects.filter(user=request.user).exists():
        first_name = Student.objects.get(user=request.user).first_name
        last_name = Student.objects.get(user=request.user).last_name
        full_name = first_name + " " + last_name

    else:
        full_name = "Admin"

    total_number_dept = Department.objects.all().count()
    total_number_student = Student.objects.all().count()
    total_number_teacher = Teacher.objects.all().count()
    total_number_staffs = Staff.objects.all().count()
    return render(
        request,
        "dashboard.html",
        {
            "name": full_name,
            "total_number_of_dept": total_number_dept,
            "total_number_of_students": total_number_student,
            "total_number_of_teachers": total_number_teacher,
            "total_number_of_staffs": total_number_staffs,
        },
    )


@login_required(login_url="login")
def institute_info_view(request):
    return render(request, "institute_info.html", {})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def students_view(request):
    # student = Student.objects.get(user=request.user)
    student = Student.objects.get(user=request.user)
    return render(request, "students.html", {"student": student})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def enrollment_view(request):

    student = Student.objects.get(user=request.user)
    query_set = Assignment.objects.filter(department=student.department)

    if request.method == "POST":
        for course in query_set:
            if str(course.id) in request.POST:
                print("hi", course.course.course_code)

                with transaction.atomic():
                    enrollment = Enrollment()
                    enrollment.student = student
                    enrollment.course = course
                    enrollment.save()

                break

    query_set = query_set.annotate(
        has_enrolled=Case(
            When(
                Exists(
                    Enrollment.objects.filter(course=OuterRef("pk"), student=student)
                ),
                then=Value(True),
            ),
            default=Value(False),
            output_field=BooleanField(),
        )
    ).annotate(
        is_approved=Case(
            When(
                Exists(
                    Enrollment.objects.filter(
                        course=OuterRef("pk"), student=student, is_approved=True
                    )
                ),
                then=Value(True),
            ),
            default=Value(False),
            output_field=BooleanField(),
        )
    )

    total_courses = query_set.count()
    total_courses_enrolled = Enrollment.objects.filter(student=student).count()

    return render(
        request,
        "enrollment.html",
        {
            "courses": list(query_set),
            "total_available_courses": total_courses,
            "courses_enrolled": total_courses_enrolled,
        },
    )


@login_required(login_url="login")
@user_passes_test(is_student, login_url="home")
def ranklist_view(request):
    student = Student.objects.get(user=request.user)

    query_set = Mark.objects.filter(
        enrollment__student__department=student.department,
        enrollment__student__session=student.session,
    )
    query_set = Enrollment.objects.filter(student=request.user.student)
    return render(request, "ranklist.html", {"courses": list(query_set)})


@login_required(login_url="login")
def staff_view(request):
    query_set = Staff.objects.all()
    return render(request, "staffs.html", {"staffs": list(query_set)})


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
def notice_board_view(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return render(request, "noticeboard.html", {"pdf": list(pdf)})


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

    query_set = Mark.objects.filter(
        enrollment__student__user=request.user, is_approved=True
    )

    if request.method == "POST":
        form = select_semester(request.POST)

        if form.is_valid():
            semester = form.cleaned_data["semester"]
            print(semester)
            if semester != 0:
                query_set = query_set.filter(enrollment__course__semester=semester)
    else:
        form = select_semester()

    if query_set.exists():
        total_credits = query_set.aggregate(
            Sum("enrollment__course__course__credit_no")
        )["enrollment__course__course__credit_no__sum"]
        print("total: ", total_credits)
        marks = list(query_set)

        sum = Decimal("0.0")
        for mark in marks:
            sum = sum + (mark.gpa * mark.enrollment.course.course.credit_no)

        print(sum)
        cgpa = sum / total_credits
        print("cgpa: ", cgpa)
    else:
        cgpa = Decimal("0.0")
        total_credits = Decimal("0.0")
    return render(
        request,
        "results.html",
        {
            "form": form,
            "marks": list(query_set),
            "cgpa": round(cgpa, 2),
            "completed_credit": round(total_credits, 2),
        },
    )


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def view_results_view(request):

    query_set = Mark.objects.filter(enrollment__course__teacher__user=request.user)

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

                    registration_no = form.cleaned_data["registration_no"]
                    student = Student.objects.get(registration_no=registration_no)

                    assignment = form.cleaned_data["course"]
                    print("hello")
                    enrollment = Enrollment.objects.filter(
                        student=student,
                        course=assignment,
                        course__year=datetime.datetime.now().year,
                    ).first()

                    print("hellllllll", enrollment)

                    mark = Mark()
                    mark.enrollment = enrollment
                    mark.term_test = form.cleaned_data["term_test"]
                    mark.attendance = form.cleaned_data["attendance"]
                    mark.total_classes = form.cleaned_data["total_classes"]
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

        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith(".csv"):
            raise TypeError("It was probably not a CSV file. Please upload a CSV file")
            # messages.error(request, "File is not CSV type")
            # return HttpResponseRedirect(reverse("csv_upload"))
            # if file is too large, return
        if csv_file.multiple_chunks():
            raise Exception(
                "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),)
            )
            # messages.error(
            #     request,
            #     "Uploaded file is too big (%.2f MB)."
            #     % (csv_file.size / (1000 * 1000),),
            # )
            # return HttpResponseRedirect(reverse("csv_upload"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        print(len(lines))
        # print("debug")

        index = 0
        try:
            for index, line in enumerate(lines):
                fields = line.split(",")

                registration_no = fields[0]
                student = Student.objects.get(registration_no=registration_no)

                enrollment = Enrollment.objects.filter(
                    student=student,
                    course__course=course,
                    year=datetime.datetime.now().year,
                ).first()

                mark = Mark()
                mark.enrollment = enrollment
                mark.term_test = Decimal(fields[1])
                mark.attendance = int(fields[2])
                mark.total_classes = int(fields[3])
                mark.semester_final = Decimal(fields[4])

                mark.save()

                # mark = Mark()
                # registration_no = int(fields[0])
                # print(index)
                # student = Student.objects.get(registration_no=registration_no)
                # # print(2)
                # mark.student = student
                # # print(3)
                # # print(4)
                # mark.course = course
                # mark.term_test = Decimal(fields[1])
                # # print(5)
                # mark.attendance = int(fields[2])
                # # print(6)
                # mark.total_attendence = int(fields[3])
                # # print(7)
                # mark.other_assesment = Decimal(fields[4])
                # # print(8)
                # mark.semester_final = Decimal(fields[5])
                # # print(9)
                # mark.save()
        except ValueError as e:
            raise ValueError(
                "CSV contains data of unexpected type at record no. "
                + str(index + 1)
                + "."
            )

        except IntegrityError as e:
            raise IntegrityError(
                "CSV may be containing duplicate record at row " + str(index + 1) + "."
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
