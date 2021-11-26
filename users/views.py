from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="login")
def home_view(request):

    return render(request, "home.html", {})


def logout_view(request):
    logout(request)
    return redirect("login")
