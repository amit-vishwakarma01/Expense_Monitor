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
    path('adminlogin',views.adminlogin,name="adminlogin"),
    path('validator',views.validator,name="validator"),
    path('admin_panel',views.admin_panel,name="admin_panel"),
    path('adminlogout',views.adminlogout,name="adminlogout"),
    path('category',views.category,name="category"),
    path('addcategory',views.addcategory,name="addcategory"),
    #path('edittype',views.edittype,name="edittype"),
    path('deletetype',views.deletetype,name="deletetype"),
    path('queries',views.queries,name="queries"),
    path('reply',views.reply,name="reply"),
    path('sendreply',views.sendreply,name="sendreply"),
    path('close',views.close,name="close"),
]
