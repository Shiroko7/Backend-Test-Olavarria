import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateMenuForm, RequestMenuForm, SchedulerForm
from .models import Menu, MealManager, MenuRequest
from django.conf import settings
from scheduler.scheduler import scheduler, slack_reminder


def view_home(request):
    return render(request, 'mealmngmt/home.html')


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
            detaillink = "{0}menu_details/{1}/".format(
                request.build_absolute_uri('/mealmngmt/'), menu.id)
            sharelink = "{0}menu/{1}/".format(
                request.build_absolute_uri('/mealmngmt/'), menu.id)
            context = {
                "form": form,
                "uuid": menu.id,
                "sharelink": sharelink,
                "detaillink": detaillink,
                "msg": "Link para compartir el menu.",
                "post": True
            }
            url = "{0}menu/{1}/".format(
                request.build_absolute_uri('/mealmngmt/'), menu.id)
            scheduler.add_job(
                slack_reminder,
                args=[settings.OPEN_HOUR, settings.CLOSE_HOUR, url, menu.id],
                trigger='interval',
                minutes=1,
                id="slack_reminder",
                max_instances=1,
                replace_existing=True,
            )
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
    form = SchedulerForm()
    context = {
        "menu": menu,
        "requests": menurequests,
        "form": SchedulerForm,
    }
    if request.method == "POST":
        form = SchedulerForm(request.POST)
        if form.is_valid():
            context = {
                "menu": menu,
                "requests": menurequests,
                "form": form,
                "msg": "recordatorio actualizado"
            }
            url = "{0}menu/{1}/".format(
                request.build_absolute_uri('/mealmngmt/'), uuid)
            scheduler.add_job(
                slack_reminder,
                args=[form.cleaned_data['initial_time'],
                      form.cleaned_data['final_time'], url, uuid],
                trigger='interval',
                minutes=form.cleaned_data['interval'],
                id="slack_reminder",
                max_instances=1,
                replace_existing=True,
            )
            return render(request, "mealmngmt/menu_details.html", context)
    return render(request, "mealmngmt/menu_details.html", context)


# employes view

def view_menu(request, uuid):
    # check if menu is avaible to choose from
    now = datetime.datetime.now()
    if settings.OPEN_HOUR <= now.hour < settings.CLOSE_HOUR:
        enabled = "enabled"
    else:
        enabled = "disabled"
    form = RequestMenuForm()
    menu = Menu.objects.get(id=uuid)
    context = {
        "form": form,
        "message": menu.message,
        "date": menu.date,
        "post": False,
        "enabled": enabled
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
