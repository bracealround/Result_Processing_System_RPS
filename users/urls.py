from django.urls import path
from . import views


# URLconf
urlpatterns = [
    path("", views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),
]
