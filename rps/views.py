from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
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

@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="home")
def upload_csv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "csv_upload.html", data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			messages.error(request,'File is not CSV type')
			return HttpResponseRedirect(reverse("csv_upload"))
        #if file is too large, return
		if csv_file.multiple_chunks():
			messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("csv_upload"))

		file_data = csv_file.read().decode("utf-8")		

		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		#for line in lines:						
		#	fields = line.split(",")
		#	data_dict = {}
		#	data_dict["name"] = fields[0]
		#	data_dict["start_date_time"] = fields[1]
		#	data_dict["end_date_time"] = fields[2]
		#	data_dict["notes"] = fields[3]
		#	try:
		#		form = EventsForm(data_dict)
		#		if form.is_valid():
		#			form.save()					
		#		else:
		#			logging.getLogger("error_logger").error(form.errors.as_json())												
		#	except Exception as e:
		#		logging.getLogger("error_logger").error(repr(e))					
		#		pass

	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		messages.error(request,"Unable to upload file. "+repr(e))

	#return HttpResponseRedirect(reverse("csv_upload"))