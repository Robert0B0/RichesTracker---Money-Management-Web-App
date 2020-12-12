from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.shortcuts import redirect, render

from ..users.views import context_add
from django.db.models import Sum, Q
from decimal import Decimal
from django.template.defaultfilters import date
import json



@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def graph_page(request):

    graphIncomesJSON = []
    graphExpensesJson = []

    total_expenses = request.user.monetaryuser.monetaryrecord_set.filter(
        Q(category='expenses') | 
        Q(category='upkeep') | 
        Q(category='unforeseen')
    )

    total_income = request.user.monetaryuser.monetaryrecord_set.filter(
        Q(category='monthly income') | 
        Q(category='dividents') | 
        Q(category='other')
    )

    income_dict = {
        '01/01/2020' : 100,
    }

    total_expenses = {
        '01/01/2020' : 100,
    }

    records = request.user.monetaryuser.monetaryrecord_set.order_by('date')
    all_dates = []
    all_outcome = []
    all_income = []
    

    for rec in records:
        all_dates.append(rec.date.strftime('%m/%d/%Y'))

    i = 0
    j = 0
    for dat in all_dates:
        if (records[i].category in 'expenses' or records[i].category in 'unforseen' or records[i].category in 'upkeep'):
            all_outcome.append(float(records[i].amount))
            i += 1
        else :
            all_outcome.append(0)
            i += 1

        if (records[j].category in 'monthly income' or records[j].category in 'dividents' or records[j].category in 'other'):
            all_income.append(float(records[j].amount))
            j += 1
        else :
            all_income.append(0)
            j += 1


    income_dates = []
    income_values = []
    incomes = request.user.monetaryuser.monetaryrecord_set.all().filter(
        Q(category='monthly income') | Q(category='dividents')     
    ).order_by('date')
    
    for i in incomes:
        income_dates.append(i.date.strftime('%m/%d/%Y'))
        income_values.append(float(i.amount))

    in_datesJSON = json.dumps(income_dates)
    in_valuesJSON = json.dumps(income_values) 
    all_datesJSON = json.dumps(all_dates)
    all_incomeJSON = json.dumps(all_income)
    all_outcomeJSON = json.dumps(all_outcome)

    expenses_dates = []
    expenses_values = []
    expenses = request.user.monetaryuser.monetaryrecord_set.all().filter(
        Q(category='expenses') | Q(category='upkeep') 
    ).order_by('date')

    for i in expenses:
        expenses_dates.append(json.dumps(i.date.strftime('%m/%d/%Y'))) 
        expenses_values.append(float(i.amount))

    ex_datesJSON = json.dumps(expenses_dates)
    ex_valuesJSON = json.dumps(expenses_values)

    context = {'income_dates': in_datesJSON, 'income_values': in_valuesJSON, 
        'all_dates': all_datesJSON, 'all_income': all_incomeJSON, 'all_outcome': all_outcomeJSON,
        'expenses_dates': ex_datesJSON, 'expenses_values': ex_valuesJSON,
        'graphIncomes': graphIncomesJSON, 'graphExpenses': graphExpensesJson }
    context = {**context_add(request), **context}
    return render(request, 'info/graph.html', context)


# Calendar
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'monetary_users'])
def calendar_page(request):
    records = request.user.monetaryuser.monetaryrecord_set.all()
    total_records = records.count()

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
            'Investment Cash': '#9c79b9',
        }
        return record_color.get(rec_type)


    for rec in records:
        rec_types.append(str(rec.category))
        rec_names.append(str(rec.naming))
        rec_start.append(json.dumps(rec.date.strftime('%Y-%m-%d')))
        rec_value.append(float(rec.amount))
        rec_color.append(color(rec.category))
        rec_id.append(rec.id)

            
    rec_types_JSON = json.dumps(rec_types)
    rec_names_JSON = json.dumps(rec_names)
    rec_start_JSON = json.dumps(rec_start)
    rec_value_JSON = json.dumps(rec_value)
    rec_total_JSON = json.dumps(int(rec_total))
    rec_color_JSON = json.dumps(rec_color)
    rec_id_JSON = json.dumps(rec_id)

    context = {
        'rec_types_JSON': rec_types_JSON,
        'rec_names_JSON': rec_names_JSON, 
        'rec_start_JSON': rec_start_JSON,
        'rec_value_JSON': rec_value_JSON,
        'rec_total_JSON': rec_total_JSON,
        'rec_color_JSON': rec_color_JSON,
        'rec_id_JSON': rec_id_JSON
    }
    context = {**context_add(request), **context}
    return render(request, 'info/Calendar.html', context)



