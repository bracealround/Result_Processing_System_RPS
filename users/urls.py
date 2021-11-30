from django.urls import path
from . import views
from rps import views as rps_views


# URLconf
urlpatterns = [
    path("", rps_views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),
]
