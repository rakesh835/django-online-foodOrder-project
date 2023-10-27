from django.urls import path

from.views import ( marketplace, vendor_detail, add_to_cart, decrease_cart, myCart,
					delete_cart_item,

			)



urlpatterns = [
    	path('', marketplace, name='marketplace'),
    	path('vendor/<slug:vendor_slug>/', vendor_detail, name='vendor_detail'),
    	path('myCart/', myCart, name='myCart'),
    	path('add_to_cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    	path('decrease_cart/<int:food_id>/', decrease_cart, name='decrease_cart'),

    	path('delete_cart_item/<int:cart_item_id>/', delete_cart_item, name='delete_cart_item')
    	

] 