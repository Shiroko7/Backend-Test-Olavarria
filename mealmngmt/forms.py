from django import forms
from django.conf import settings


class CreateMenuForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class RequestMenuForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    option = forms.CharField(widget=forms.Textarea)
    customization = forms.CharField(widget=forms.Textarea)


class SchedulerForm(forms.Form):
    initial_time = forms.IntegerField(initial=settings.OPEN_HOUR)
    final_time = forms.IntegerField(initial=settings.CLOSE_HOUR)
    interval = forms.IntegerField(initial=60)
