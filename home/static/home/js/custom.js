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
					response.cart_amount['tax_dict'],
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
						response.cart_amount['tax_dict'],
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
						response.cart_amount['tax_dict'],
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
	function cartAmount(tax_dict, subtotal, total){
		$('#subtotal').html(subtotal)
		$('#total').html(total)

		for (key1 in tax_dict){
			for (key2 in tax_dict[key1]){
				$('#tax-'+key1).html(tax_dict[key1][key2])
			}
		}
	}


	// Adding opening and closing hours
	$('.add_hour').on('click', function(e){
		e.preventDefault();
		var day = document.getElementById('id_day').value
		var from_hour = document.getElementById('id_from_hour').value
		var to_hour = document.getElementById('id_to_hour').value
		var is_closed = document.getElementById('id_is_closed').checked
		var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
		var url = document.getElementById('add_hour_url').value

		console.log(day, from_hour, to_hour, is_closed, csrf_token)

		if (is_closed){
			is_closed = 'True'
			condition = "day != ''"
		}else{
			is_closed = 'False'
			condition = "day != '' && from_hour != '' && to_hour != ''"
		}

		if(eval(condition)){
			$.ajax({
				type: 'POST',
				url: url,
				data: {
					'day': day,
					'from_hour': from_hour,
					'to_hour': to_hour,
					'is_closed': is_closed,
					'csrfmiddlewaretoken': csrf_token,
				},
				success: function(response){
					if(response.status == 'success'){
						if(response.is_closed == "Closed"){
							html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td><b>Closed</b></td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>'	
						}else{
							html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>'	
						}
						
						$(".opening_hours").append(html)
						document.getElementById("opening_hours").reset();
					}else{
						swal(response.message, '', 'error')
					}
				}
			})
		}else{
			swal("Please fill all fields", '', 'info')
		}
	})


	// remove opening hour
	$(document).on('click', '.remove_hour', function(e){
		e.preventDefault();

		url = $(this).attr('data-url');

		$.ajax({
			type: 'GET',
			'url': url,
			success: function(response){
				if (response.status == 'success'){
					document.getElementById('hour-'+response.id).remove()
				}
			}
		})
	})
});