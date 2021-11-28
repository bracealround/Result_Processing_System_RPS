from django.shortcuts import render

# Create your views here.
def students(request):
    return render(request,'rps/students.html')


def teachers(request):
    return render(request,'rps/teachers.html')