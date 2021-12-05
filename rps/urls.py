from django.urls import path
from . import views


# URLconf
urlpatterns = [
    path("", views.home_view, name="home"),
    path("students/", views.students_view, name="students"),
    path("teachers/", views.teachers_view, name="teachers"),
    path("results/", views.results_view, name="result"),
    path("results/view", views.view_results_view, name="view-results"),
    path("results/edit", views.edit_results_view, name="edit-results"),
    path("results/upload/csv/", views.upload_csv, name="csv_upload"),
    path("institute/department/", views.department_view, name="department"),
    path("institute/teacher/", views.institute_teacher_view, name="institute_teacher"),
    path(
        "students/edit_profile/",
        views.edit_students_profile_view,
        name="edit_students_profile",
    ),
    path(
        "teachers/edit_profile/",
        views.edit_teachers_profile_view,
        name="edit_teachers_profile",
    ),
]
