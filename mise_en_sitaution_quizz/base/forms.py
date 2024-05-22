from django import forms
from .models import Controller

class ControllerForm(forms.ModelForm):
    class Meta:
        model = Controller
        fields = ['name', 'type', 'request_infos', 'api_route']

