from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


# URLconf
urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
