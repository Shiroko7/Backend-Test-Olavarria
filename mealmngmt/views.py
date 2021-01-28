from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MenuForm
from .models import Menu, MealManager
import datetime


@login_required
def create_menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            date = datetime.date.today()
            mealmanager = MealManager.objects.get(user=request.user)
            Menu.objects.create(
                message=message,
                date=date,
                mealmanager=mealmanager
            )
            return redirect("mealmngmt:menu")
    context = {
        "form": form
    }
    return render(request, "mealmngmt/create_menu.html", context)


def view_menu(request):
    menu = Menu.objects.last()
    context = {
        "message": menu.message,
        "date": menu.date
    }
    return render(request, "mealmngmt/menu.html", context)
