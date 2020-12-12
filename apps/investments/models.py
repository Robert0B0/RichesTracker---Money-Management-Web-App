from django.db import models
from ..users.models import monetaryUser
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

# Create your models here.

class growthInvestment(models.Model):
    user = models.ForeignKey(monetaryUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, blank=True, default="Invest-Plan")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    current_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    monthly_contribution = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    interest_rate = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, 
                                        validators=[MinValueValidator(Decimal(0.1)), 
                                                   MaxValueValidator(Decimal(100))])
    time_length = models.IntegerField(null=False, default=10)
    end_result = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, default=0)

    # def end_result(self):
    #     result = current_amount * monthly_contribution * time_length
    #     return result
    
    def __str__(self):
        return str(self.naming)




