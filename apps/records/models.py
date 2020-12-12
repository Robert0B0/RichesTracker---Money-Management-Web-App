from django.db import models
from django.utils.timezone import now
from ..users.models import monetaryUser

# Create your models here.



class monetaryRecord(models.Model):
    CATEGORY = (
                ('Outcome', (
                                ('expenses', 'Expenses'),
                                ('upkeep', 'Upkeep'),
                                ('unforeseen', 'Unforeseen'),
                                ('Goal Complete', 'Goal Complete'),
                                ('Investment', 'Investment'),
                                ('Saving tipped', 'Saving tipped')
                            )
                ),
                ('Income', (
                                ('monthly income', 'Monthly Income'),
                                ('dividents', 'Dividents'),
                                ('saving funds', 'Saving Funds'),
                                ('Investment Cash', 'Investment Cash'),
                                ('other', 'Other'),
                            )
                ),
                
                
            )
    
    user = models.ForeignKey(monetaryUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, blank=True, default="Record")
    category = models.CharField(max_length=200, null=False, choices=CATEGORY, default='Outcome')
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=False, null=True, default=now)

    def __str__(self):
        return '$' + str(self.amount)
  