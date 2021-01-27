from django.shortcuts import render


def create_menu(request):
    return render(request, "mealmngmt/create_menu.html")
