from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Budget, Income, Expense
from django.db.models import Sum
from .forms import BudgetForm, IncomeForm, ExpenseForm
from .models import Profile
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.password_validation import validate_password

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')

class CustomSignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Get the password and password confirmation from the form
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')

        # Validate the password
        try:
            validate_password(password1, self.request.user)
        except ValidationError as error:
            form.add_error('password1', error)

        # Check if the passwords match
        if password1 != password2:
            form.add_error('password2', "Passwords don't match")

        # Call the parent class's form_valid method to save the user
        response = super().form_valid(form)

        return response


class CustomLogoutView(LogoutView):
    next_page = 'home'

@login_required

def dashboard(request):
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)
    last_week_start = today - timedelta(days=7)
    last_month_start = date(today.year, today.month - 1, 1)
    last_year_start = date(today.year - 1, 1, 1)
    this_year_start = date(today.year, 1, 1)
    this_month_start = date(today.year, today.month, 1)
    this_week_start = today - timedelta(days=today.weekday())

    today_total = Expense.objects.filter(user=request.user, date=today).aggregate(total=Sum('amount'))['total'] or 0
    yesterday_total = Expense.objects.filter(user=request.user, date=yesterday).aggregate(total=Sum('amount'))['total'] or 0
    last_week_total = Expense.objects.filter(user=request.user, date__range=[last_week_start, this_week_start - timedelta(days=1)]).aggregate(total=Sum('amount'))['total'] or 0
    last_month_total = Expense.objects.filter(user=request.user, date__range=[last_month_start, this_month_start - timedelta(days=1)]).aggregate(total=Sum('amount'))['total'] or 0
    last_year_total = Expense.objects.filter(user=request.user, date__range=[last_year_start, this_year_start - timedelta(days=1)]).aggregate(total=Sum('amount'))['total'] or 0
    this_year_total = Expense.objects.filter(user=request.user, date__range=[this_year_start, today]).aggregate(total=Sum('amount'))['total'] or 0
    this_month_total = Expense.objects.filter(user=request.user, date__range=[this_month_start, today]).aggregate(total=Sum('amount'))['total'] or 0
    this_week_total = Expense.objects.filter(user=request.user, date__range=[this_week_start, today]).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'today_total': today_total,
        'yesterday_total': yesterday_total,
        'last_week_total': last_week_total,
        'last_month_total': last_month_total,
        'last_year_total': last_year_total,
        'this_year_total': this_year_total,
        'this_month_total': this_month_total,
        'this_week_total': this_week_total,
    }

    return render(request, 'dashboard.html', context)




@login_required
def report(request):
    budgets = Budget.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    categories = set([b.category for b in budgets])
    data = []
    for category in categories:
        budget = budgets.filter(category=category).first()
        if budget:
            total_expenses = expenses.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
            data.append({
                'category': category,
                'budget': budget.amount,
                'expenses': total_expenses,
                'remaining': budget.remaining,
            })
    return render(request, 'report.html', {'data': data})

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def incomes_list(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'incomes_list.html', {'incomes': incomes})

def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('incomes_list')
    else:
        form = IncomeForm()
    return render(request, 'create_income.html', {'form': form})

def edit_income(request, pk):
    income = Income.objects.get(pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('incomes_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'edit_income.html', {'form': form})

def delete_income(request, pk):
    income = Income.objects.get(pk=pk)
    if request.method == 'POST':
        income.delete()
        return redirect('incomes_list')
    return render(request, 'delete_income.html', {'income': income})

def budgets_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'budgets_list.html', {'budgets': budgets})

def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budgets_list')
    else:
        form = BudgetForm()
    return render(request, 'create_budget.html', {'form': form})

def edit_budget(request, pk):
    budget = Budget.objects.get(pk=pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budgets_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'edit_budget.html', {'form': form})

def delete_budget(request, pk):
    budget = Budget.objects.get(pk=pk)
    if request.method == 'POST':
        budget.delete()
        return redirect('budgets_list')
    return render(request, 'delete_budget.html', {'budget': budget})

@login_required
def expenses_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses_list.html', {'expenses': expenses})


@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('expenses_list')
    else:
        form = ExpenseForm()
    return render(request, 'create_expense.html', {'form': form})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('expenses_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, id=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
        return redirect('expenses_list')
    return render(request, 'delete_expense.html', {'expense': expense})
