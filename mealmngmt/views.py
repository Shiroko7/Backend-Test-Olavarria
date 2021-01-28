from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MenuForm
from .models import Menu, MealManager
import datetime


@login_required
def create_menu(request):

    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            date = datetime.date.today()
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
                "msg": "Link para compartir el menu."
            }
            return render(request, "mealmngmt/create_menu.html", context)
    else:
        form = MenuForm()
        context = {
            "form": form
        }
        return render(request, "mealmngmt/create_menu.html", context)


def view_menu(request, uuid):
    menu = Menu.objects.get(id=uuid)
    context = {
        "message": menu.message,
        "date": menu.date
    }
    return render(request, "mealmngmt/menu.html", context)
