from django.forms import ModelForm
from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class GoalForm(ModelForm):
    class Meta:
        model = monetaryGoals
        fields = '__all__'
        # fields = ['naming', 'category', 'amount', 'due_date']
        widgets = {
            'due_date': DateInput()
        }

