from django import forms


class MenuForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
