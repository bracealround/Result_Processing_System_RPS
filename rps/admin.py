from django.contrib import admin
from .models import Student, Teacher, Department, Course, Mark


class MarkAdmin(admin.ModelAdmin):

    list_display = ("student", "course", "final_result", "gpa")

    exclude = ("gpa", "grade")

   

class StudentAdmin(admin.ModelAdmin):

    list_display = ("registration_no", "department", "session")

    exclude = ()

    # fieldsets = ((None, {"fields": ("")}),)


class TeacherAdmin(admin.ModelAdmin):

    list_display = ("first_name", "last_name", "department", "title")

    exclude = ()

class DepartmentAdmin(admin.ModelAdmin):

    list_display = ("dept_code", "dept_name")

    exclude = ()

class CourseAdmin(admin.ModelAdmin):

    list_display = ("course_name", "department", "teacher")

    exclude = ()

# Register your models here.
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Mark, MarkAdmin)
