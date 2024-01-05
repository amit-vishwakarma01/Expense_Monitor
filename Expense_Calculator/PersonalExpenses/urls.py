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
path('personaldashboard',views.personaldashboard,name='personaldashboard'),
path('viewgroup',views.viewgroup,name='viewgroup'),
path('showaddpersonform',views.showaddpersonform,name='showaddpersonform'),
path('addgroup',views.addgroup,name='addgroup'),
path('addtransaction',views.addtransaction,name='addtransaction'),
path('addtrans',views.addtrans,name='addtrans'),
path('viewtrans',views.viewtrans,name='viewtrans'),
path('updatetrans',views.updatetrans,name='updatetrans'),
path('deletetrans',views.deletetrans,name='deletetrans'),
path('editgroup',views.editgroup,name='editgroup'),
path('deletegroup',views.deletegroup,name='deletegroup'),
path('updategroupdetail',views.updategroupdetail,name='updategroupdetail'),
path('sendemail',views.sendemail,name='sendemail')
]
