from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.shortcuts import redirect, render

from django.db.models import Sum, Q
from decimal import Decimal

from .forms import *
from .models import *
from ..users.views import context_add

from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def record_page(request):
    

    total_expenses = request.user.monetaryuser.monetaryrecord_set.filter(
        category='expenses').aggregate(Sum('amount'))['amount__sum']
    total_upkeep = request.user.monetaryuser.monetaryrecord_set.filter(
        category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_unforeseen = request.user.monetaryuser.monetaryrecord_set.filter(
        category='unforeseen').aggregate(Sum('amount'))['amount__sum']
    total_income = request.user.monetaryuser.monetaryrecord_set.filter(
        category='monthly income').aggregate(Sum('amount'))['amount__sum']
    total_dividents = request.user.monetaryuser.monetaryrecord_set.filter(
        category='dividents').aggregate(Sum('amount'))['amount__sum']
    total_in_other = request.user.monetaryuser.monetaryrecord_set.filter(
        category='other').aggregate(Sum('amount'))['amount__sum']

    if total_expenses is None:
        total_expenses = 0
    if total_upkeep is None:
        total_upkeep = 0
    if total_unforeseen is None:
        total_unforeseen = 0
    if total_income is None:
        total_income = 0
    if total_dividents is None:
        total_dividents = 0
    if total_in_other is None:
        total_in_other = 0

    expenses_records = request.user.monetaryuser.monetaryrecord_set.filter(category='expenses')
    unforeseen_records = request.user.monetaryuser.monetaryrecord_set.filter(category='unforeseen')
    upkeep_records = request.user.monetaryuser.monetaryrecord_set.filter(category='upkeep')
    Investment_records = request.user.monetaryuser.monetaryrecord_set.filter(category='Investment')
    saving_tip = request.user.monetaryuser.monetaryrecord_set.filter(category='Saving tipped')

    InvestmentCash = request.user.monetaryuser.monetaryrecord_set.filter(category='Investment Cash')
    saving_funds = request.user.monetaryuser.monetaryrecord_set.filter(category='Saving Funds')
    monthlyincome_records = request.user.monetaryuser.monetaryrecord_set.filter(category='monthly income')
    dividents_records = request.user.monetaryuser.monetaryrecord_set.filter(category='dividents')
    others = request.user.monetaryuser.monetaryrecord_set.filter(category='other')


    context = {
        'total_expenses': total_expenses, 'total_upkeep': total_upkeep,
        'total_unforeseen': total_unforeseen, 'total_income': total_income,
        'total_dividents': total_dividents, 'total_in_other': total_in_other,
        'expenses_records': expenses_records, 'unforeseen_records': unforeseen_records,
        'upkeep_records': upkeep_records, 'Investment_records': Investment_records,
        'monthlyincome_records': monthlyincome_records, 'dividents_records': dividents_records,
        'others': others, 'saving_tip': saving_tip, 'saving_funds': saving_funds
        }
    context = {**context_add(request), **context}
    return render(request, 'records/record_page.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def create_record(request):
    user = request.user.monetaryuser
    create_record_form = RecordForm( initial = { 'user': user })
    if request.method == 'POST':
        create_record_form = RecordForm(request.POST)
        if create_record_form.is_valid:
            create_record_form.save()
            return redirect('/records/')

    context = {'create_record_form': create_record_form}
    context = {**context_add(request), **context}
    return render(request, 'records/record_create.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def update_record(request, pk):
    record = monetaryRecord.objects.get(id=pk)
    update_record_form = RecordForm(instance=record)
    if request.method == 'POST':
        update_record_form = RecordForm(request.POST, instance=record)
        if update_record_form.is_valid:
            update_record_form.save()
            return redirect('/records/')

    context = {'update_record_form': update_record_form, 'record': record}
    context = {**context_add(request), **context}
    return render(request, 'records/record_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def delete_record(request, pk):
    record = monetaryRecord.objects.get(id=pk)
    user = request.user.monetaryuser
    worth = request.user.monetaryuser.min_worth
    if request.method == 'POST':
        if record.category in 'expenses' or record.category in 'upkeep' or record.category in 'unforeseen':
            user.min_worth = worth - record.amount
        else:
            user.min_worth = worth + record.amount
        user.save()
        record.delete()
        return redirect('/records/')

    context = {'record': record}
    context = {**context_add(request), **context}
    return render(request, 'records/record_delete.html', context)



@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def create_record_modal(request):
    data = dict()
    user = request.user
    if request.method == 'POST':
        create_record_form = RecordForm( initial = { 'user' : user })
        if create_record_form.is_valid():
            create_record_form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = RecordForm()

    context = {'create_record_form': create_record_form}
    data['html_form'] = render_to_string('records/record_add.html',
        context,
        request=request,
    )
    return JsonResponse(data)










