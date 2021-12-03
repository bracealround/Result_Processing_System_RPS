from django.urls import path
from . import views


# URLconf
urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
]
