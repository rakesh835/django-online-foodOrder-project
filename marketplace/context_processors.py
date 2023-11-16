from .models import Cart, Tax



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
	tax = 0
	subtotal = 0
	total = 0
	tax_dict = {}
	if request.user.is_authenticated:
		cart = Cart.objects.filter(user=request.user)

		for item in cart:
			subtotal += item.fooditem.price * item.quantity

		get_tax = Tax.objects.filter(is_active=True)

		for i in get_tax:
			tax_type = i.tax_type
			tax_percentage = i.tax_percentage
			tax_amount = round((tax_percentage * subtotal)/100, 2)
			tax_dict.update({tax_type: {str(tax_percentage): tax_amount}})

		tax = sum(x for key in tax_dict.values() for x in key.values())
		total = subtotal + tax

		return dict(tax=tax, subtotal=subtotal, total=total, tax_dict=tax_dict)

	else:
		return dict(tax=tax, subtotal=subtotal, total=total, tax_dict=tax_dict)


