from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.shortcuts import redirect, render

from django.db.models import Sum, Q
from decimal import Decimal

from .forms import *
from .models import *
from ..users.views import context_add
from ..records.models import monetaryRecord
from _datetime import date



# Create your views here.
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def savings_page(request):
    jars = request.user.monetaryuser.savingsjar_set.all()
    total_savings = jars.count()

    context = {'jars': jars, 'total_savings': total_savings}
    context = {**context_add(request), **context}
    return render(request, 'savings/savings_page.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def create_saving(request):
    user = request.user.monetaryuser
    form = SavingsForm( initial = { 'user': user })
    if request.method == 'POST':
        form = SavingsForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/savings/savings/')
            
    context = {'form': form}
    context = {**context_add(request), **context}
    return render(request, 'savings/savings_create.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def update_saving(request, pk):
    jar = savingsJar.objects.get(id=pk)
    form = SavingsForm(instance=jar)
    if request.method == 'POST':
        form = SavingsForm(request.POST, instance=jar)
        if form.is_valid:
            form.save()
            return redirect('/savings/savings/')

    context = {'form': form, 'jar': jar}
    context = {**context_add(request), **context}
    return render(request, 'savings/savings_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def delete_saving(request, pk):
    jar = savingsJar.objects.get(id=pk)
    if request.method == 'POST':
        jar.delete()
        return redirect('/savings/savings/')

    context = {'jar': jar}
    context = {**context_add(request), **context}
    return render(request, 'savings/savings_delete.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def break_saving(request, pk):
    jar = savingsJar.objects.get(id=pk)
    user = request.user.monetaryuser
    if request.method == 'POST':
        record = monetaryRecord.objects.create(
                user=user,
                naming="Funds from " + jar.naming,
                category='Saving Funds',
                amount=jar.amount,
                date=date.today()
             )
        record.save()
        jar.delete()
        return redirect('/savings/savings/')

    context = {'jar': jar}
    context = {**context_add(request), **context}
    return render(request, 'savings/savings_break.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def tip_saving(request, pk):
    jar = savingsJar.objects.get(id=pk)
    user = request.user.monetaryuser
    jar_amount = jar.amount
    tip = 10
    if request.method == 'POST':
        tip = request.POST.get('tip-value')

        record = monetaryRecord.objects.create(
                user=user,
                naming="Tipped " + jar.naming,
                category='Saving tipped',
                amount=tip,
                date=date.today()
             )
        record.save()
       
        jar.amount = jar_amount + Decimal(tip)
        jar.save()
        return redirect('/savings/savings/')

    context = {'tip': tip, 'jar': jar}
    context = {**context_add(request), **context}
    return render(request, 'savings/savings_tip.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def tip_all_savings(request):
    jars = request.user.monetaryuser.savingsjar_set.all()
    jar_all = Decimal(jars.count())
    user = request.user.monetaryuser
    tip = 10
    if request.method == 'POST':
        tip = request.POST.get('tip-value')
        
        record = monetaryRecord.objects.create(
                user=user,
                naming="Tipped all Savings",
                category='Saving tipped',
                amount=tip,
                date=date.today()
             )
        record.save()

        tip_ration = (Decimal(tip) / jar_all)
        for jar in jars:
            jar_amount = jar.amount
            jar.amount = jar_amount + tip_ration
            jar.save()
        return redirect('/savings/savings/')

    context = {'tip': tip, 'jars': jars, 'jar_all': jar_all}
    context = {**context_add(request), **context}
    return render(request, 'savings/savings_tip_all.html', context)

