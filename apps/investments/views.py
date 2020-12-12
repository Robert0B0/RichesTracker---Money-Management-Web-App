from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.shortcuts import redirect, render

from django.db.models import Sum, Q
from decimal import Decimal

from .forms import *
from .models import *
from ..users.views import context_add
from _datetime import date
from ..records.models import monetaryRecord

# Create your views here.

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def investments_page(request):
    investments = request.user.monetaryuser.growthinvestment_set.all()
    total_invs = investments.count()

    def compound_interest(principle, rate, time):
        result = principle * (pow((1 + rate / 100), time))
        return result

    def investment_annually_return(current_year, year_created, rate, amount):
        if current_year > year_created:
            for year_created in current_year:
                year_created += 1
                amount = amount * rate
        result = amount
        return result

    for investment in investments:
        investment.end_result = compound_interest(
                                        investment.current_amount,
                                        investment.interest_rate,
                                        investment.time_length)
        investment.save()

    context = {'investments': investments, 'total_invs': total_invs}
    context = {**context_add(request), **context}
    return render(request, 'investments/investments_page.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def investment_create(request):
    user = request.user.monetaryuser
    form = InvestmentForm(initial={'user': user})
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/investments/investments/')
            
    context = {'form': form}
    context = {**context_add(request), **context}
    return render(request, 'investments/investment_create.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def investment_update(request, pk):
    plan = growthInvestment.objects.get(id=pk)
    form = InvestmentForm(instance=plan)
    if request.method == 'POST':
        form = InvestmentForm(request.POST, instance=plan)
        if form.is_valid:
            form.save()
            return redirect('/investments/investments/')

    context = {'form': form, 'plan': plan}
    context = {**context_add(request), **context}
    return render(request, 'investments/investment_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def investment_delete(request, pk):
    plan = growthInvestment.objects.get(id=pk)
    user = request.user.monetaryuser
    
    if request.method == 'POST':
        

        plan.delete()
        return redirect('/investments/investments/')

    context = {'plan': plan}
    context = {**context_add(request), **context}
    return render(request, 'investments/investment_delete.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def investment_invest(request, pk):
    plan = growthInvestment.objects.get(id=pk)
    user = request.user.monetaryuser
    
    plan_amount = plan.current_amount
    amount = 10
    if request.method == 'POST':
        amount = request.POST.get('value')
        
        record = monetaryRecord.objects.create(
                user=user,
                naming="Invested in " + plan.naming,
                category='Investment',
                amount=amount,
                date=date.today()
             )
        record.save()

        plan.current_amount = plan_amount + Decimal(amount)
        plan.save()
        return redirect('/investments/investments/')

    context = {'amount': amount, 'plan': plan}
    context = {**context_add(request), **context}
    return render(request, 'investments/investment_invest.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def investment_invest_all(request):
    plans = request.user.monetaryuser.growthinvestment_set.all()
    plan_all = Decimal(plans.count())
    user = request.user.monetaryuser
    
    tip = 10
    if request.method == 'POST':
        tip = request.POST.get('tip-value')
        
        record = monetaryRecord.objects.create(
                user=user,
                naming="Invested in all plans",
                category='Investment',
                amount=tip,
                date=date.today()
             )
        record.save()

        tip_ration = (Decimal(tip) / plan_all)
        for plan in plans:
            plan_amount = plan.current_amount
            plan.current_amount = plan_amount + tip_ration
            plan.save()
        return redirect('/investments/investments/')

    context = {'tip': tip, 'plans': plans, 'plan_all': plan_all}
    context = {**context_add(request), **context}
    return render(request, 'investments/investment_invest_all.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def investment_cash_out(request, pk):
    plan = growthInvestment.objects.get(id=pk)
    user = request.user.monetaryuser
    
    plan_amount = plan.current_amount
    value = 10
    if request.method == 'POST':
        value = request.POST.get('cash-value')
        plan.current_amount = plan_amount - Decimal(value)
        plan.save()

        record = monetaryRecord.objects.create(
                user=user,
                naming='Investment Cash',
                category='Investment Cash',
                amount=value,
                date=date.today()
             )
        record.save()
        
        return redirect('/investments/investments/')

    context = {'plan': plan, 'value': value}
    context = {**context_add(request), **context}
    return render(request, 'investments/investment_cash-out.html', context)

