from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class monetaryUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, default='Username')
    min_worth = models.DecimalField(null=False, max_digits=7, decimal_places=2, default=10.00)
    monthly_income = models.DecimalField(null=False, max_digits=7, decimal_places=2, default=10.00)
    warning_amount = models.DecimalField(null=False, max_digits=7, decimal_places=2, default=10.00)
    email = models.EmailField(max_length=200, null=True, default='mail@mail.mail')
    profile_pic = models.ImageField(default="profile-default.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class bugReport(models.Model):
    PAGE = (
        ('HOME', 'HOME'), 
        ('RECORDS', 'RECORDS'),
        ('GOALS', 'GOALS'),
        ('SAVINGS','SAVINGS'),
        ('INVESTMENTS', 'INVESTMENTS'),
        ('CALENDAR', 'CALENDAR'),
        ('GRAPH', 'GRAPH'),
        ('SETTINGS', 'SETTINGS'),
        ('NAVIGATION', 'NAVIGATION'),
        ('ABOUT','ABOUT'),
    )
    
    user = models.ForeignKey(monetaryUser, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    page = models.CharField(max_length=200, null=False, choices=PAGE, default='HOME') 
    details = models.CharField(max_length=1000, null=False, blank=True, default="BugReport")


    def __str__(self):
        return str(self.page)
