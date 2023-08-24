from django.urls import path

from .views import (registerUser, login_user, logout_user, 
                    customerDashboard, myAccount, activate,
                    user_account_activation_link_confirmation,
                    forgot_password, reset_password_validate, reset_password

            )



urlpatterns = [
    path('registerUser/', registerUser, name='registerUser'),
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    path('myAccount/', myAccount, name='myAccount'),
    path('customerDashboard/', customerDashboard, name='customerDashboard'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('user_account_activation_link_confirmation/', user_account_activation_link_confirmation, name='user_account_activation_link_confirmation'),

    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', reset_password_validate, name='reset_password_validate'),
    path('reset_password/', reset_password, name='reset_password'),

] 