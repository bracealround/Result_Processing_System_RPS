from django.shortcuts import render

# Create your views here.
def students(request):
    return render(request,'rps/students.html')


def teachers(request):
    return render(request,'rps/teachers.html')

def results(request):
    return render(request,'rps/results.html')

def teacher_results(request):
    return render(request,'rps/teacher_results.html')