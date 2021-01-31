from django import forms
from django.conf import settings
from .models import Menu, MenuRequest


class CreateMenuModelForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = {
            'message',
            'date'
        }
        widgets = {
            'message': forms.Textarea,
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class CreateMenuRequestModelForm(forms.ModelForm):
    class Meta:
        model = MenuRequest
        fields = {
            'first_name',
            'last_name',
            'option',
            'customization'
        }
        widgets = {
            'message': forms.Textarea,
            'date': forms.Textarea
        }


class SchedulerForm(forms.Form):
    initial_time = forms.IntegerField(initial=settings.OPEN_HOUR)
    final_time = forms.IntegerField(initial=settings.CLOSE_HOUR)
    interval = forms.IntegerField(initial=60)
