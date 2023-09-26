from django import forms

from .models import Robot


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']
