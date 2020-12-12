from django.forms import ModelForm
from django import forms
from .models import *


class InvestmentForm(ModelForm):
    class Meta:
        model = growthInvestment
        fields = '__all__'
