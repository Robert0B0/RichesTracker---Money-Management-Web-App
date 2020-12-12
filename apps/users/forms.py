from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import DateTimeInput

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MonetaryUserForm(ModelForm):
    class Meta:
        model = monetaryUser
        fields = '__all__'
        exclude = ['user']


class BugForm(ModelForm):
    class Meta:
        model = bugReport
        fields = '__all__'
        widgets = {
            'details': forms.Textarea(attrs={'cols': 40, 'rows': 10}),
        }
