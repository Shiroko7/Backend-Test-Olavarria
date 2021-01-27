from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def create_menu(request):
    return render(request, "mealmngmt/create_menu.html")
