from django.urls import path

from .views import (registerUser, login_user, logout_user, 
                    customerDashboard, myAccount

            )



urlpatterns = [
    path('registerUser/', registerUser, name='registerUser'),
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    path('myAccount/', myAccount, name='myAccount'),
    path('customerDashboard/', customerDashboard, name='customerDashboard'),
    
] 