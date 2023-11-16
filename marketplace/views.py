from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.db.models import Prefetch
from django.http import JsonResponse
from django.db.models import Q
from datetime import date, datetime

from vendor.models import Vendor, OpeningHour
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

	opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
	
	today_date = date.today()
	weekday = today_date.isoweekday()

	current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=weekday)


	if request.user.is_authenticated:
		cart = Cart.objects.filter(user=request.user)
	else:
		cart = None

	context = {
			'vendor': vendor,
			'categories': categories,
			'cart': cart,
			'opening_hours': opening_hours,
			'current_opening_hours': current_opening_hours,
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




def search(request):
	address = request.GET.get('address')
	keyword = request.GET.get('restaurant_name')
	latitude = request.GET.get('latitude')
	longitude = request.GET.get('longitude')
	radius = request.GET.get('radius')


	vendors_by_fooditem = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
	vendors = Vendor.objects.filter(Q(id__in=vendors_by_fooditem) | Q(vendor_name__icontains=keyword, user__is_active=True, is_approved=True))

	vendors_count = vendors.count()

	context = {
			'vendors': vendors,
			'vendors_count': vendors_count,
	}

	return render(request, 'marketplace/listings.html', context)