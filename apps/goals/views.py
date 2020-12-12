from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.shortcuts import redirect, render

from django.db.models import Sum, Q
from decimal import Decimal

from .forms import *
from .models import *
from ..users.views import context_add

import datetime
from ..records.models import monetaryRecord
from _datetime import date


# Create your views here.

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def goals_page(request):
    goals = request.user.monetaryuser.monetarygoals_set.all()
    comp_goals = request.user.monetaryuser.completedmonetarygoals_set.all()
    total_comp = comp_goals.count()
    
    
    
    context = {'goals': goals, 'comp_goals': comp_goals, 'total_comp': total_comp}
    context = {**context_add(request), **context}
    return render(request, 'goals/goals_page.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def create_goal(request):
    user = request.user.monetaryuser
    form = GoalForm( initial = { 'user': user })
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/goals/goals/')

    context = {'form': form}
    context = {**context_add(request), **context}
    return render(request, 'goals/goal_create.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def update_goal(request, pk):
    goal = monetaryGoals.objects.get(id=pk)
    form = GoalForm(instance=goal)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid:
            form.save()
            return redirect('/goals/goals/')

    context = {'form': form, 'goal': goal}
    context = {**context_add(request), **context}
    return render(request, 'goals/goal_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def complete_goal(request, pk):
    goal = monetaryGoals.objects.get(id=pk)
    user = request.user.monetaryuser
    if request.method == 'POST':
        comp_goal = completedmonetaryGoals(
                    user=goal.user,
                    naming=goal.naming,
                    category=goal.category,
                    amount=goal.amount,
                    date_created=goal.date_created,
                    due_date=datetime.date.today(),
        )
        comp_goal.save() 

        record = monetaryRecord.objects.create(
                user=user,
                naming="Completed " + goal.naming,
                category='Goal Complete',
                amount=goal.amount,
                date=date.today()
             )
        record.save()

        goal.delete()
        return redirect('/goals/goals/')

    context = {'goal': goal}
    context = {**context_add(request), **context}
    return render(request, 'goals/goal_complete.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def delete_goal(request, pk):
    goal = monetaryGoals.objects.get(id=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('/goals/goals/')
        
    context = {'goal': goal}
    context = {**context_add(request), **context}
    return render(request, 'goals/goal_delete.html', context)

