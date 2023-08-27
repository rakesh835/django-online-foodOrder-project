from django.urls import path

from .views import (registerVendor, vendorDashboard,
                vendor_account_activation_link_confirmation,
                vendor_profile
    )
from accounts.views import activate


urlpatterns = [
    path('', vendorDashboard, name='vendorDashboard'),
    path('profile/', vendor_profile, name='vendor_profile'),
    path('registerVendor/', registerVendor, name='registerVendor'),
    path('vendorDashboard/', vendorDashboard, name='vendorDashboard'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('vendor_account_activation_link_confirmation/', vendor_account_activation_link_confirmation, name='vendor_account_activation_link_confirmation'),

] 