from django.contrib import admin

from .models import Student, Teacher, Department, Course, Mark, Semester

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Mark)
admin.site.register(Semester)
