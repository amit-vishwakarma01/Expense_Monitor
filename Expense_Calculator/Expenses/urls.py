from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
path('dashboard',views.dashboard,name='dashboard'),
path('myprofile',views.myprofile,name='myprofile'),
path('profile',views.profile,name='profile'),
path('addexpense',views.addexpense,name='addexpense'),
path('addingitem',views.addingitem,name='addingitem'),
path('showexpense',views.showexpense,name='showexpense'),
path('expense',views.expense,name='expense'),
path('edit',views.edit,name='edit'),
path('contact',views.contact,name='contact'),
path('update_item',views.update_item,name='update_item'),
path('delete',views.delete,name='delete'),
path('submitquery',views.submitquery,name='submitquery'),
path('showexpensebydate',views.showexpensebydate,name="showexpensebydate"),
path('deleteaccount',views.deleteaccount,name="deleteaccount"),
path('userquery',views.userquery,name="userquery"),
path('userreply',views.userreply,name="userreply"),
path('senduserreply',views.senduserreply,name="senduserreply"),
path('userclose',views.userclose,name="userclose"),


    
]