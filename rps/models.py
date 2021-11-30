from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext as _

# Create your models here.
# Department table
class Department(models.Model):
    dept_code = models.CharField(max_length=3, unique=True, null=True)
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.dept_name) + " ( " + str(self.dept_code) + " )"


# # Student table (ManyToMany relation to be built with Course)
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_no = models.IntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    session = models.CharField(max_length=20)

    def __str__(self):
        return (
            str(self.first_name)
            + " "
            + str(self.last_name)
            + " ( "
            + str(self.registration_no)
            + " )"
        )


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)


# Course table (ManyToMany relation to be built with Students)
class Course(models.Model):
    course_code = models.CharField(primary_key=True, max_length=20)
    course_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    credit_no = models.DecimalField(max_digits=20, decimal_places=2)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)

    def __str__(self):
        return (
            str(self.course_name)
            + " ( "
            + str(self.course_code)
            + " )"
            + str(self.department)
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course_code", "department", "semester"],
                name="unique_subject",
            )
        ]
        ordering = ["department", "semester", "course_code"]
        # unique_together = (('course_code', 'course_dept_code','sem'),)


# Mark table
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    term_test = models.DecimalField(max_digits=20, decimal_places=2)
    attendance = models.IntegerField(default=0)
    total_attendence = models.IntegerField(default=0)
    other_assesment = models.DecimalField(max_digits=20, decimal_places=2)
    semester_final = models.DecimalField(max_digits=20, decimal_places=2)
    final_result = models.DecimalField(max_digits=20, decimal_places=2)
    # current_cr=models.IntegerField(default=0)
    @property
    def final_result(self):
        final_result = (
            self.term_test
            + (self.attendance / self.total_attendence) * 10
            + self.other_assesment
            + (self.semester_final) * 0.6
        )
        return final_result

    def __str__(self):
        return str(self.student) + " ( " + str(self.course) + " )"

    class Meta:
        unique_together = (("student", "course"),)


# # result table
# class result(models.Model):
#     result_registration_no = models.ForeignKey(Student, on_delete=models.CASCADE)
#     sem1 = models.FloatField(default=0)
#     sem2 = models.FloatField(default=0)
#     sem3 = models.FloatField(default=0)
#     sem4 = models.FloatField(default=0)
#     sem5 = models.FloatField(default=0)
#     sem6 = models.FloatField(default=0)
#     sem7 = models.FloatField(default=0)
#     sem8 = models.FloatField(default=0)
#     ogpa = models.FloatField(default=0)
#     previous_grades = models.FloatField(default=0)
#     total_credits = models.IntegerField(default=0)
#     result_status = models.TextField(max_length=30, default="None")

#     def __str__(self):
#         return (
#             str(self.result_registration_no)
#             + " Sem1 = "
#             + str(self.sem1)
#             + " Sem2 = "
#             + str(self.sem2)
#             + " Sem3 = "
#             + str(self.sem3)
#             + " Sem4 = "
#             + str(self.sem4)
#             + " Sem5 = "
#             + str(self.sem5)
#             + " Sem6 = "
#             + str(self.sem6)
#             + " Sem7 = "
#             + str(self.sem7)
#             + " Sem8 = "
#             + str(self.sem8)
#             + " OGPA = "
#             + str(self.ogpa)
#             + " Result Status = "
#             + str(self.result_status)
#         )
