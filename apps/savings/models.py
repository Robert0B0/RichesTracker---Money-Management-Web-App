from django.db import models
from ..users.models import monetaryUser

# Create your models here.


class savingsJar(models.Model):
    
    user = models.ForeignKey(monetaryUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, blank=True, default="Savings-Jar")
    desired_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.naming)


class brokenSavingsJar(models.Model):
    
    user = models.ForeignKey(monetaryUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, blank=True, default="Savings-Jar")
    desired_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.naming)
