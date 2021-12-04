from django.contrib import admin
from .models import Student, Teacher, Department, Course, Mark


class MarkAdmin(admin.ModelAdmin):

    list_display = ()

    exclude = ("gpa", "grade")

    # fieldsets = ((None, {"fields": ("")}),)


# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Mark, MarkAdmin)
