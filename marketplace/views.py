from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from django.http import JsonResponse
import decimal

from vendor.models import Vendor
from menu.models import Category, FoodItem
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amount

# Create your views here.


def marketplace(request):
	vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
	vendors_count = vendors.count()

	context = {
			'vendors': vendors,
			'vendors_count': vendors_count,
	}

	return render(request, 'marketplace/listings.html', context)



def vendor_detail(request, vendor_slug):
	vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
	categories = Category.objects.filter(vendor=vendor).prefetch_related(
		Prefetch(
				'fooditems',
				queryset = FoodItem.objects.filter(is_available=True)
			)
		)
	
	if request.user.is_authenticated:
		cart = Cart.objects.filter(user=request.user)
	else:
		cart = None

	context = {
			'vendor': vendor,
			'categories': categories,
			'cart': cart,
	}

	return render(request, 'marketplace/vendor_detail.html', context)




def add_to_cart(request, food_id):
	if request.user.is_authenticated:
		if request.headers.get('x-requested-with') == 'XMLHttpRequest':
			# Check if food item exists
			try:
				fooditem = FoodItem.objects.get(id=food_id)
			
				# Check if the user has already added food to the cart
				try:
					chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)

					# increase cart quantity
					chkCart.quantity += 1
					chkCart.save()
					return JsonResponse({'status': 'Success', 'message': 'Increase the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)})
				
				except:
					chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
					return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty': 1, 'cart_amount': get_cart_amount(request)})
				
			except:
				return JsonResponse({'status': 'Failed', 'message': 'This food item does not exists!'})
		
		else:
			return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
	else:
		return JsonResponse({'status': 'Failed', 'message': 'Please login to continue'})




def decrease_cart(request, food_id):
	if request.user.is_authenticated:
		if request.headers.get('x-requested-with') == 'XMLHttpRequest':
			# Check if food item exists
			try:
				fooditem = FoodItem.objects.get(id=food_id)
			
				# Check if the user has added this food to the cart
				try:

					chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
					
					# decrease cart quantity
					chkCart.quantity -= 1
					
					if chkCart.quantity == 0:
						chkCart.delete()
						return JsonResponse({'status': 'Success', 'message': 'Decrease the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': 0, 'cart_amount': get_cart_amount(request)})
					
					chkCart.save()
					return JsonResponse({'status': 'Success', 'message': 'Decrease the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)})
				
				except:
					return JsonResponse({'status': 'Failed', 'message': 'This food item is not added to the cart'})
				
			except:
				return JsonResponse({'status': 'Failed', 'message': 'This food item does not exists!'})
		
		else:
			return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
	else:
		return JsonResponse({'status': 'Failed', 'message': 'Please login to continue'})




def myCart(request):
	
	if request.user.is_authenticated:
		cart = Cart.objects.filter(user=request.user).order_by('-created_at')

		context = {
				'cart': cart,
		}

		return render(request, 'marketplace/myCart.html', context)
	else:
		return redirect('home')



def delete_cart_item(request, cart_item_id):
	if request.user.is_authenticated:
		if request.headers.get('x-requested-with') == 'XMLHttpRequest':
			# Check if food item exists
			try:
				fooditem = Cart.objects.get(user=request.user, id=cart_item_id)
				
				if fooditem:
					fooditem.delete()
					return JsonResponse({'status': 'Success', 'message': 'Cart item is deleted', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amount(request)})
			except:
				return JsonResponse({'status': 'Failed', 'message': 'Item does not found in cart'})
		else:
			return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})	
	else:
		return JsonResponse({'status': 'Failed', 'message': 'Please login to continue'})