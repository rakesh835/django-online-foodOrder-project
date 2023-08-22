from django.urls import path

from .views import registerVendor, vendorDashboard



urlpatterns = [
    path('registerVendor/', registerVendor, name='registerVendor'),
    path('vendorDashboard/', vendorDashboard, name='vendorDashboard'),
] 