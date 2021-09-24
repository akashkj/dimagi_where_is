from django import forms


class LocationAddForm(forms.Form):
    email = forms.EmailField()
    location = forms.CharField(max_length=30)


class LocationQueryForm(forms.Form):
    email = forms.EmailField()
