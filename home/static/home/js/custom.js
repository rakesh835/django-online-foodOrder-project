$(document).ready(function(){
	$('.add_to_cart').on('click', function(e){
		e.preventDefault();

		food_id = $(this).attr('data-id');
		url = $(this).attr('data-url');

		data = {
			food_id: food_id,
		}
		$.ajax({
			type: 'GET',
			url: url,
			data: data,
			success: function(response){
				$('#cart_counter').html(response.cart_counter['cart_count']);
				$('#qty-'+food_id).html(response.qty);

				cartAmount(
					response.cart_amount['tax'],
					response.cart_amount['subtotal'],
					response.cart_amount['total']
				);
			}
		})
	})




	$('.item_qty').each(function(){
		var the_id = $(this).attr('id')
		var qty = $(this).attr('data-qty')
		console.log(qty)
		$('#'+the_id).html(qty)
	})


	// decrease the quantity of cart item
	$('.decrease_cart').on('click', function(e){
		e.preventDefault();

		food_id = $(this).attr('data-id');
		url = $(this).attr('data-url');
		cart_id = $(this).attr('id');

		data = {
			food_id: food_id,
		}
		$.ajax({
			type: 'GET',
			url: url,
			data: data,
			success: function(response){
				console.log(response)

				if (response.status === 'Failed'){
					console.log(response)
					swal(response.message, "", "error");
				}else{
					$('#cart_counter').html(response.cart_counter['cart_count']);
					$('#qty-'+food_id).html(response.qty);
					
					cartAmount(
						response.cart_amount['tax'],
						response.cart_amount['subtotal'],
						response.cart_amount['total']
					);

					removeCartItem(response.qty, cart_id);
					checkCartEmpty();
				}
				
			}
		})
	})


	// Delete cart item
	$('.delete_cart_item').on('click', function(e){
		e.preventDefault();

		cart_item_id = $(this).attr('data-id');
		url = $(this).attr('data-url');

		$.ajax({
			type: 'GET',
			url: url,
			success: function(response){
				console.log(response)

				if (response.status == 'Failed'){
					swal(response.message, "", "error");
				}else{
					$('#cart_counter').html(response.cart_counter['cart_count']);

					cartAmount(
						response.cart_amount['tax'],
						response.cart_amount['subtotal'],
						response.cart_amount['total']
					);

					removeCartItem(0, cart_item_id);
					checkCartEmpty();
				}
				
			}
		})
	})


	// remove the cart item when quantity is 0
	function removeCartItem(cartItemQty, cart_id){
		if (cartItemQty <= 0){
			document.getElementById("cart-item-"+cart_id).remove()
		}
	}


	// check if cart is empty and then display message
	function checkCartEmpty(){
		var cart_counter = document.getElementById('cart_counter').innerHTML;
		console.log(cart_counter)
		if (cart_counter == 0){
			document.getElementById("empty-cart").style.display = "block";
		}
	}



	// increase or decrease cart amount
	function cartAmount(tax, subtotal, total){
		$('#tax').html(tax)
		$('#subtotal').html(subtotal)
		$('#total').html(total)
	}

});