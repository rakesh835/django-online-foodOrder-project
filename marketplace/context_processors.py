from .models import Cart



def get_cart_counter(request):
	cart_count = 0

	if request.user.is_authenticated:
		try:
			cart = Cart.objects.filter(user=request.user)

			if cart:
				for cart_item in cart:
					cart_count += cart_item.quantity
			else:
				cart_count = 0
		except:
			cart_count = 0
	else:
		cart_count = 0

	return dict(cart_count=cart_count)



def get_cart_amount(request):
	if request.user.is_authenticated:
		cart = Cart.objects.filter(user=request.user)

		tax = 0
		subtotal = 0
		total = 0

		for item in cart:
			subtotal += item.fooditem.price * item.quantity

		total = subtotal + tax

		return dict(tax=tax, subtotal=subtotal, total=total)

