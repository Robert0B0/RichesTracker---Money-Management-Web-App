from django import forms
from django.forms import ModelForm
from django.forms import DateTimeInput


from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class RecordForm(ModelForm):
    class Meta:
        model = monetaryRecord
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }

