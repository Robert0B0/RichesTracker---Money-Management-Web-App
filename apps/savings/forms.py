from django.forms import ModelForm
from django import forms
from .models import *


class SavingsForm(ModelForm):
    class Meta:
        model = savingsJar
        fields = '__all__'