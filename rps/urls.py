from django.urls import path
from . import views


# URLconf
urlpatterns = [
    path('students/', views.students, name='rps-students'),
    path('teachers/', views.teachers, name='rps-teachers'),
]
