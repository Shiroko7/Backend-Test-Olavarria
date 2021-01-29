from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateMenuForm, RequestMenuForm
from .models import Menu, MealManager, MenuRequest
import datetime

# Manager views


@login_required
def create_menu(request):
    if request.method == "POST":
        form = CreateMenuForm(request.POST)
        if form.is_valid():
            # form values
            message = form.cleaned_data['message']
            date = form.cleaned_data['date']

            # session values
            mealmanager = MealManager.objects.get(user=request.user)
            menu = Menu.objects.create(
                message=message,
                date=date,
                mealmanager=mealmanager
            )
            newlink = "{0}menu/{1}/".format(
                request.build_absolute_uri('/mealmngmt/'), menu.id)
            context = {
                "form": form,
                "uuid": menu.id,
                "newlink": newlink,
                "msg": "Link para compartir el menu.",
                "post": True
            }
            return render(request, "mealmngmt/create_menu.html", context)
    else:
        form = CreateMenuForm()
        context = {
            "form": form,
            "post": False
        }
        return render(request, "mealmngmt/create_menu.html", context)


@login_required
def menu_list(request):
    menus = Menu.objects.all()
    context = {
        "menus": menus
    }
    return render(request, "mealmngmt/menu_list.html", context)


@login_required
def menu_details(request, uuid):
    menu = Menu.objects.get(id=uuid)
    menurequests = MenuRequest.objects.filter(menu=menu)
    context = {
        "menu": menu,
        "requests": menurequests,
    }
    return render(request, "mealmngmt/menu_details.html", context)


# employes view

def view_menu(request, uuid):
    form = RequestMenuForm()
    menu = Menu.objects.get(id=uuid)
    context = {
        "form": form,
        "message": menu.message,
        "date": menu.date,
        "post": False,
    }
    if request.method == "POST":
        form = RequestMenuForm(request.POST)
        if form.is_valid():
            # form values
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            option = form.cleaned_data['option']
            customization = form.cleaned_data['customization']

            menurequest = MenuRequest.objects.create(
                first_name=first_name,
                last_name=last_name,
                option=option,
                customization=customization,
                menu=menu
            )
            context = {
                "form": form,
                "msg": "Solicitud enviada.",
                "post": True
            }
            return render(request, "mealmngmt/menu.html", context)
    return render(request, "mealmngmt/menu.html", context)
