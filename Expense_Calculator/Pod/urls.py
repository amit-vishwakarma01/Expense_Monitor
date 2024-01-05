from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
path('pods',views.pods,name='pods'),
path('addpod',views.addpod,name='addpod'),
path('addingpod',views.addingpod,name='addingpod'),
path('poddetail',views.poddetail,name='poddetail'),
path('searchmember',views.searchmember,name='searchmember'),
path('searchmemberdetail',views.searchmemberdetail,name='searchmemberdetail'),
path('adduser',views.adduser,name='adduser'),
path('removeuser',views.removeuser,name='removeuser'),
path('addtransaction',views.addtransaction,name='addtransaction'),
path('addtransactiondata',views.addtransactiondata,name='addtransactiondata'),
path('updategroupdetail',views.updategroupdetail,name='updategroupdetail'),
path('deletegroup',views.deletegroup,name='deletegroup'),
path('viewtransaction',views.viewtransaction,name='viewtransaction'),
path('Updatetransaction',views.Updatetransaction,name='Updatetransaction'),
path('deletepodtransaction',views.deletepodtransaction,name='deletepodtransaction'),
path('sendmail',views.sendmail,name='sendmail'),
path('showtempuserform',views.showtempuserform,name='showtempuserform')
]