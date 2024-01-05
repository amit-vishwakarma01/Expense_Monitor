"""Expense_Calculator URL Configuration

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
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('submitquery1',views.submitquery1,name="submitquery1"),
    path('home/',views.home,name="home"),
    path('authentication/',include('authentication.urls')),
    path('Expenses/',include('Expenses.urls')),
    path('admin_panel/',include('admin_panel.urls')),
    path('Pod/',include('Pod.urls')),
    path('PersonalExpenses/',include('PersonalExpenses.urls')),
    path('admin/', admin.site.urls),
]
