from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from calendar import isleap
from datetime import date

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    frequency_choices = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    frequency = models.CharField(max_length=10, choices=frequency_choices, default='monthly')
    amount_per_frequency = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.category}: {self.amount_per_frequency} ({self.frequency})"

    def is_leap_year(self, year):
        return isleap(year)

    @property
    def amount(self):
        if self.frequency == 'daily':
            return self.amount_per_frequency * (self.end_date - self.start_date).days
        elif self.frequency == 'weekly':
            return self.amount_per_frequency * ((self.end_date - self.start_date).days // 7)
        elif self.frequency == 'monthly':
            return self.amount_per_frequency
        elif self.frequency == 'yearly':
            num_days = 366 if self.is_leap_year(self.start_date.year) else 365
            return self.amount_per_frequency / num_days

    @property
    def remaining(self):
        expenses = Expense.objects.filter(user=self.user, budget=self)
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        remaining = self.amount - total_expenses
        return remaining



class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    frequency_choices = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    frequency = models.CharField(max_length=10, choices=frequency_choices, default='monthly')
    date = models.DateField()

    def __str__(self):
        return f"{self.source}: {self.amount} ({self.frequency})"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True, blank=True, default=None)
    date = models.DateField()

    def __str__(self):
        return f"{self.category}: {self.amount}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

