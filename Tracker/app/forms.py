
from django import forms
from .models import Income, Expense, Budget

class BudgetForm(forms.ModelForm):
    frequency_choices = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    frequency = forms.ChoiceField(choices=frequency_choices, initial='monthly', widget=forms.Select(attrs={'class': 'form-control'}))
    amount_per_frequency = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Budget
        fields = ['amount_per_frequency', 'category', 'frequency', 'amount_per_frequency', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_per_frequency': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'frequency', 'date']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'budget', 'date']
