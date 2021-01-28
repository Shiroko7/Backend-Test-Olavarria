from django import forms


class CreateMenuForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))


class RequestMenuForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    option = forms.CharField(widget=forms.Textarea)
    customization = forms.CharField(widget=forms.Textarea)
