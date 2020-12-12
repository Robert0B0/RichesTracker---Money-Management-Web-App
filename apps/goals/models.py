from django.db import models
from ..users.models import monetaryUser

# Create your models here.


class monetaryGoals(models.Model):
    CATEGORY = (
                ('Small Goal', 'Small Goal'),
                ('Liability Goal', 'Liability Goal'),
                ('Life Goal', 'Life Goal'),
                ('Investment Goal', 'Investment Goal'),
                )

    user = models.ForeignKey(monetaryUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, default='Goal')
    category = models.CharField(max_length=200, null=False, choices=CATEGORY, default='Small Goal')
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    due_date = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return str(self.naming)


class completedmonetaryGoals(models.Model):
    CATEGORY = (
                ('Small Goal', 'Small Goal'),
                ('Liability Goal', 'Liability Goal'),
                ('Life Goal', 'Life Goal'),
                ('Investment Goal', 'Investment Goal'),
                )

    user = models.ForeignKey(monetaryUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, default='Completed-Goal')
    category = models.CharField(max_length=200, null=False, choices=CATEGORY, default='Small Goal')
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    due_date = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return str(self.naming)

