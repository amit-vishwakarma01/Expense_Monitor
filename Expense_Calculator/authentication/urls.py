from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('update_profile',views.update_profile,name='update_profile'),
    path('change_password',views.change_password,name='change_password'),
    path('updating_password',views.updating_password,name="updating_password"),
    path('authenticate_user',views.authenticate_user,name='authenticate_user'),
    path('tempuserregister',views.tempuserregister,name='tempuserregister')
]