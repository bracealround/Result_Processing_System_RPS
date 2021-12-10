from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Student, Teacher, Department, Course, Assignment, Enrollment, Mark


class MarkAdmin(admin.ModelAdmin):

    list_display = ("enrollment", "final_result", "gpa", "grade", "is_approved")

    @property
    def exclude(self):
        if 1 < 3:
            return ("gpa", "grade")
        else:
            print("hhh")
            return ("grade",)

    actions = ["approve"]

    @admin.action(description="Approve Result")
    def approve(self, request, queryset):

        for mark in queryset:
            mark.is_approved = True
            mark.save()

        print("test passed")

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     super().save_model(request, obj, form, change)


class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "registration_no",
        "department",
        "session",
        "user",
        "link_to_Department",
    )

    exclude = ()

    ordering = [
        "registration_no",
        "department",
        "session",
        "user",
    ]

    def link_to_Department(self, obj):
        link = reverse(
            "admin:rps_department_change", args=[obj.department.id]
        )  # model name has to be lowercase
        return format_html('<a href="%s">%s</a>' % (link, obj.department.dept_name))

    link_to_Department.allow_tags = True
    link_to_Department.short_description = "department"

    # fieldsets = ((None, {"fields": ("")}),)


class AssignmentAdmin(admin.ModelAdmin):

    list_display = ("course", "department", "teacher", "year")

    exclude = ()


class EnrollmentAdmin(admin.ModelAdmin):

    list_display = ("student", "course", "teacher", "is_approved")

    exclude = ()

    def teacher(self, obj):
        print(obj)

        return obj.course.teacher

    actions = ["approve"]

    @admin.action(description="Approve Enrollment")
    def approve(self, request, queryset):

        for enrollment in queryset:
            enrollment.is_approved = True
            enrollment.save()

        print("test passed")


class TeacherAdmin(admin.ModelAdmin):

    list_display = ("first_name", "last_name", "department", "title")

    exclude = ()


class DepartmentAdmin(admin.ModelAdmin):

    list_display = ("dept_code", "dept_name")

    exclude = ()


class CourseAdmin(admin.ModelAdmin):

    list_display = ("course_code", "course_name", "department")

    exclude = ()


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Mark, MarkAdmin)
