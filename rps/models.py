from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext as _
from decimal import *
from rps.result import calculate_gpa_and_grade

# Create your models here.
# Department table
class Department(models.Model):
    dept_code = models.CharField(max_length=3, unique=True, null=True)
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.dept_name) + " ( " + str(self.dept_code) + " )"


# Student table (ManyToMany relation to be built with Course)
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
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
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)

    def __str__(self):
        return (
            str(self.first_name)
            + " "
            + str(self.last_name)
            + " ( "
            + str(self.department.dept_code)
            + " )"
        )


class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    contact_no = models.IntegerField()

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)


# Course table (ManyToMany relation to be built with Students)
class Course(models.Model):
    course_code = models.CharField(unique=True, max_length=20)
    course_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    credit_no = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.course_code)


# Assignment of a teacher to a course in a particular year
class Assignment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    semester = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return str(self.course) + " for " + str(self.department.dept_code)

    class Meta:
        unique_together = (("department", "course", "semester", "year"),)


# Enrollment
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return (
            str(self.student.registration_no)
            + "-"
            + str(self.course.course.course_code)
            + " by "
            + str(self.course.teacher)
        )

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)

        # save original values, when model is loaded from database,
        # in a separate attribute on the model
        instance._loaded_values = dict(zip(field_names, values))

        return instance

    def save(self, *args, **kwargs):

        if not self._state.adding and (
            self._loaded_values["is_approved"] == True and self.is_approved == False
        ):
            print('"is_approved" cannot be set to False once set to True.')
            self.is_approved = True

        super().save(*args, **kwargs)

    class Meta:
        unique_together = (("student", "course"),)


# Mark table
class Mark(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    term_test = models.DecimalField(max_digits=20, decimal_places=2)
    attendance = models.IntegerField(default=0)
    total_classes = models.IntegerField(default=0)
    semester_final = models.DecimalField(max_digits=20, decimal_places=2)
    final_result = models.DecimalField(max_digits=20, decimal_places=2)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    grade = models.CharField(max_length=2, null=True)
    is_approved = models.BooleanField(default=False)

    @property
    def final_result(self):
        final_result = (
            round(
                Decimal(
                    (
                        self.term_test
                        + Decimal((self.attendance / self.total_classes) * 10)
                        + (self.semester_final) * Decimal("0.7")
                    )
                )
                / Decimal("0.5")
            )
            * 0.5
        )

        return final_result

    def __str__(self):
        return str(self.enrollment.student) + " ( " + str(self.enrollment.course) + " )"

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)

        # save original values, when model is loaded from database,
        # in a separate attribute on the model
        instance._loaded_values = dict(zip(field_names, values))

        return instance

    def save(self, *args, **kwargs):
        self.gpa, self.grade = calculate_gpa_and_grade(self.final_result)

        if not self._state.adding and (
            self._loaded_values["is_approved"] == True and self.is_approved == False
        ):
            print('"is_approved" cannot be set to False once set to True.')
            self.is_approved = True

        super().save(*args, **kwargs)


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
