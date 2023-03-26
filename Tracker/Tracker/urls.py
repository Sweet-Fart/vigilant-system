"""Tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import CustomLoginView, CustomSignUpView
from app.views import home  
from app import views
from app.views import CustomLogoutView
from app.views import profile
from app.views import expenses_list, incomes_list, budgets_list, edit_expense, delete_expense, edit_budget, delete_budget, delete_income, edit_income, create_budget, create_expense, create_income


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('budget/create/', create_budget, name='create_budget'),
    path('income/create/', create_income, name='create_income'),
    path('expense/create/', create_expense, name='create_expense'),
    path('', views.home, name='home'),
    #path('signup/', views.signup, name='signup'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #path('budget/', views.budget, name='budget'),
    #path('income/', views.income, name='income'),
    #path('expense/', views.expense, name='expense'),
    path('report/', views.report, name='report'),

    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),

    path('expenses/', expenses_list, name='expenses_list'),
    path('incomes/', incomes_list, name='incomes_list'),
    path('budgets/', budgets_list, name='budgets_list'),

    path('expenses/edit/<int:pk>/', edit_expense, name='edit_expense'),
    path('expenses/delete/<int:pk>/', delete_expense, name='delete_expense'),
    path('incomes/edit/<int:pk>/', edit_income, name='edit_income'),
    path('incomes/delete/<int:pk>/', delete_income, name='delete_income'),
    path('budgets/edit/<int:pk>/', edit_budget, name='edit_budget'),
    path('budgets/delete/<int:pk>/', delete_budget, name='delete_budget'),

]

