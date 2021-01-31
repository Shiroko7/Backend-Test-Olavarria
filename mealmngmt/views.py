import datetime

from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from .forms import CreateMenuModelForm, CreateMenuRequestModelForm, SchedulerForm
from .models import Menu, MealManager, MenuRequest

from scheduler.scheduler import scheduler, slack_reminder


class HomeView(generic.TemplateView):
    template_name = 'mealmngmt/home.html'


# Manager views

class MenuCreateView(generic.CreateView):
    template_name = 'mealmngmt/create_menu.html'
    form_class = CreateMenuModelForm
    uuid = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['msg'] = "Link para compartir el menu."
        context['detaillink'] = "{0}menu_details/{1}/".format(
            self.request.build_absolute_uri('/mealmngmt/'), self.uuid)
        context['sharelink'] = "{0}menu/{1}/".format(
            self.request.build_absolute_uri('/mealmngmt/'), self.uuid)
        context['uuid'] = self.uuid
        if self.uuid != "":
            context['post'] = True
        else:
            context['post'] = False

        return context

    def form_valid(self, form):
        menu = form.save(commit=False)
        menu.mealmanager = MealManager.objects.get(user=self.request.user)
        menu.save()
        self.uuid = menu
        context = self.get_context_data()

        scheduler.add_job(
            slack_reminder,
            args=[settings.OPEN_HOUR, settings.CLOSE_HOUR,
                  context['sharelink'], menu.id],
            trigger='interval',
            minutes=1,
            id="slack_reminder",
            max_instances=1,
            replace_existing=True,
        )

        return self.render_to_response(context)


class MenuListView(generic.ListView):
    template_name = "mealmngmt/menu_list.html"
    queryset = Menu.objects.all()


class MenuDetailView(generic.FormView):
    template_name = "mealmngmt/menu_details.html"
    form_class = SchedulerForm
    msg = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = Menu.objects.get(id=self.kwargs['pk'])
        context["menu"] = menu
        context["requests"] = MenuRequest.objects.filter(menu=menu)
        context['msg'] = self.msg

        return context

    def form_valid(self, form):
        url = "{0}menu/{1}/".format(
            self.request.build_absolute_uri('/mealmngmt/'), self.kwargs['pk'])
        self.msg = "recordatorio actualizado"
        context = self.get_context_data()
        scheduler.add_job(
            slack_reminder,
            args=[form.cleaned_data['initial_time'],
                  form.cleaned_data['final_time'], url, self.kwargs['pk']],
            trigger='interval',
            minutes=form.cleaned_data['interval'],
            id="slack_reminder",
            max_instances=1,
            replace_existing=True,
        )
        return self.render_to_response(context)

# User View


class MenuRequestView(generic.CreateView):
    template_name = 'mealmngmt/menu.html'
    form_class = CreateMenuRequestModelForm
    msg = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.datetime.now()
        if settings.OPEN_HOUR <= now.hour < settings.CLOSE_HOUR:
            context['enabled'] = "enabled"
        else:
            context['enabled'] = "enabled"

        context['menu'] = Menu.objects.get(id=self.kwargs['pk']).message
        context['msg'] = self.msg

        return context

    def form_valid(self, form):
        menurequest = form.save(commit=False)
        menurequest.menu = Menu.objects.get(id=self.kwargs['pk'])
        menurequest.save()
        self.msg = "Solicitud enviada."
        context = self.get_context_data()

        return self.render_to_response(context)
