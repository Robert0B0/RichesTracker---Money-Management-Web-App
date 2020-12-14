from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.shortcuts import redirect, render

from django.db.models import Sum, Q
from decimal import Decimal

from .forms import *
from .models import *

from ..records.forms import RecordForm
from ..goals.forms import GoalForm

from ..records.models import monetaryRecord
from ..goals.models import monetaryGoals

import json



@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='monetary_users')
            user.groups.add(group)
            monetaryUser.objects.create(
                user=user,
                name=username,
                min_worth=100,
                monthly_income=1000,
                email=form.cleaned_data.get('email'),
             )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user-settings')
            # messages.success(request, 'Account was created for ' + username)
            # return redirect('login_page')
    context = {'form': form}
    return render(request, 'users/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect.')
    context = {}
    return render(request, 'users/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def settings_page(request):
    monetaryuser = request.user.monetaryuser
    records = request.user.monetaryuser.monetaryrecord_set.all()
    if records.count() == 0:
        monetaryRecord.objects.create(
            user = monetaryuser,
            naming = 'Welcome',
            amount= 100,
            category='other'
        )

    form = MonetaryUserForm(instance=monetaryuser)
    
    if request.method == 'POST':
        form = MonetaryUserForm(request.POST, request.FILES, instance=monetaryuser)
        if form.is_valid():
            form.save()
            return redirect('/setting/')

    context = {'form': form}
    context = {**context_add(request), **context}
    return render(request, 'users/user_settings.html', context)


# Global #

def context_add(request):
    records = request.user.monetaryuser.monetaryrecord_set.all()
    goals = request.user.monetaryuser.monetarygoals_set.all()
    total_records = records.count()
    total_goals = goals.count()
    user_name = request.user.username
    warning = request.user.monetaryuser.warning_amount
    jars = request.user.monetaryuser.savingsjar_set.all()
    total_jars = jars.count()

    total_expenses = request.user.monetaryuser.monetaryrecord_set.filter(
        Q(category='expenses') | 
        Q(category='upkeep') | 
        Q(category='unforeseen') |
        Q(category='Goal Complete') |
        Q(category='Investment') |
        Q(category='Saving tipped') 
    ).aggregate(Sum('amount'))['amount__sum']

    total_income = request.user.monetaryuser.monetaryrecord_set.filter(
        Q(category='monthly income') | 
        Q(category='dividents') | 
        Q(category='other') |
        Q(category='saving funds')
    ).aggregate(Sum('amount'))['amount__sum']

    if total_expenses is None:
        total_expenses = 0
    if total_income is None:
        total_income = 0

    balance = total_income - total_expenses

    user = request.user.monetaryuser
    create_record_form = RecordForm(initial={'user': user})
    if request.method == 'POST':
        create_record_form = RecordForm(request.POST)
        if create_record_form.is_valid:
            create_record_form.save()
            return redirect('/home/')



    context = {
        'records': records, 'total_records': total_records,
        'jars': jars, 'total_jars': total_jars,
        'goals': goals, 'total_goals': total_goals, 'user_name': user_name,
        'balance': balance, 'warning': warning,
        'create_record_form': create_record_form,
        }

    return context

# HOME PAGE #
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def home_page(request):
    records = request.user.monetaryuser.monetaryrecord_set.all()
    goals = request.user.monetaryuser.monetarygoals_set.order_by("due_date")[:5]
    total_records = records.count()
    total_goals = request.user.monetaryuser.monetarygoals_set.count()
    user_name = request.user.username
    warning = request.user.monetaryuser.warning_amount
    jars = request.user.monetaryuser.savingsjar_set.order_by("amount")[:5]
    total_jars = request.user.monetaryuser.savingsjar_set.count()

    total_expenses = request.user.monetaryuser.monetaryrecord_set.filter(
        Q(category='expenses') | 
        Q(category='upkeep') | 
        Q(category='unforeseen') |
        Q(category='Goal Complete') |
        Q(category='Investment') |
        Q(category='Saving tipped') 
    ).aggregate(Sum('amount'))['amount__sum']

    total_income = request.user.monetaryuser.monetaryrecord_set.filter(
        Q(category='monthly income') | 
        Q(category='dividents') | 
        Q(category='other') |
        Q(category='saving funds')
    ).aggregate(Sum('amount'))['amount__sum']

    if total_expenses is None:
        total_expenses = 0
    if total_income is None:
        total_income = 0

    balance = total_income - total_expenses

    user = request.user.monetaryuser
    create_record_form = RecordForm(initial={'user': user})
    if request.method == 'POST':
        create_record_form = RecordForm(request.POST)
        if create_record_form.is_valid:
            create_record_form.save()
            return redirect('/home/home/')

    expenses_records = request.user.monetaryuser.monetaryrecord_set.filter(category='expenses')
    unforeseen_records = request.user.monetaryuser.monetaryrecord_set.filter(category='unforeseen')
    upkeep_records = request.user.monetaryuser.monetaryrecord_set.filter(category='upkeep')
    Investment_records = request.user.monetaryuser.monetaryrecord_set.filter(category='Investment')

    monthlyincome_records = request.user.monetaryuser.monetaryrecord_set.filter(category='monthly income')
    dividents_records = request.user.monetaryuser.monetaryrecord_set.filter(category='dividents')
    others = request.user.monetaryuser.monetaryrecord_set.filter(category='other')

    rec_types = []
    rec_names = []
    rec_start = []
    rec_value = []
    rec_color = []
    rec_id = []
    rec_total = total_records

    def color(rec_type):
        record_color={
            'expenses': '#8f3737',
            'upkeep': '#c36363',
            'unforeseen': '#ff9650',
            'monthly income': '#2cce34',
            'other': '#509e7e',
            'Saving tipped': '#8b9530',
            'Saving Funds': '#8b5ab3',
            'goal complete': '#a3883b',
            'dividents': '#47428b',
            'Investment': '#9b9540',
            'Investment Cash': '#9c79b9'
        }
        return record_color.get(rec_type)


    for rec in records:
        rec_types_JSON = json.dumps(rec_types)
        rec_types.append(str(rec.category))
        rec_names.append(str(rec.naming))
        rec_start.append(json.dumps(rec.date.strftime('%Y-%m-%d')))
        rec_value.append(float(rec.amount))
        rec_color.append(color(rec.category))
        rec_id.append(rec.id)

    rec_names_JSON = json.dumps(rec_names)
    rec_start_JSON = json.dumps(rec_start)
    rec_value_JSON = json.dumps(rec_value)
    rec_total_JSON = json.dumps(int(rec_total))
    rec_color_JSON = json.dumps(rec_color)
    rec_id_JSON = json.dumps(rec_id)

    context = {
        'records': records, 'total_records': total_records,
        'jars': jars, 'total_jars': total_jars,
        'goals': goals, 'total_goals': total_goals, 'user_name': user_name,
        'balance': balance, 'warning': warning,
        
        'create_record_form': create_record_form,
        'expenses_records': expenses_records, 'unforeseen_records': unforeseen_records,
        'upkeep_records': upkeep_records, 'Investment_records': Investment_records,
        'monthlyincome_records': monthlyincome_records, 'dividents_records': dividents_records,
        'others': others,

        'rec_types_JSON': rec_types_JSON,
        'rec_names_JSON': rec_names_JSON, 
        'rec_start_JSON': rec_start_JSON,
        'rec_value_JSON': rec_value_JSON,
        'rec_total_JSON': rec_total_JSON,
        'rec_color_JSON': rec_color_JSON,
        'rec_id_JSON': rec_id_JSON
        }
    context = {**context_add(request), **context}
    return render(request, 'users/home.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def about_page(request):
    

    context={}
    context = {**context_add(request), **context}
    return render(request, 'users/about.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def bugs_page(request):
    user = request.user.monetaryuser
    bug_form = BugForm(initial={'user': user})
    if request.method == 'POST':
        bug_form = BugForm(request.POST)
        if bug_form.is_valid:
            bug_form.save()
            return redirect('/bugs/')

    context={'bug_form': bug_form}
    context = {**context_add(request), **context}
    return render(request, 'users/bug_report.html', context)

