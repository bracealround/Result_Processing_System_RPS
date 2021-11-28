from django.urls import path
from . import views


# URLconf
urlpatterns = [
    path('students/', views.students, name='rps-students'),
    path('results/', views.results, name='rps-result'),
    path('teachers/', views.teachers, name='rps-teachers'),
    path('teachers/results/', views.teacher_results, name='rps-teacher_results'),
    path('teachers/results/individual', views.teacher_results, name='rps-teacher_results_individual'),
]
