from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from vendor.models import Vendor
from .models import Category, FoodItem
from vendor.utils import get_vendor
from .forms import CategoryForm, FoodItemForm
from vendor.views import check_role_vendor

# Create your views here.


@user_passes_test(check_role_vendor)
def menu_builder(request):
	vendor = get_vendor(request)
	categories = Category.objects.filter(vendor=vendor).order_by('-updated_at')

	context = {
			'categories': categories,
	}
	return render(request, 'menu/menu_builder.html', context)


@user_passes_test(check_role_vendor)
def food_item_by_category(request, pk=None):
	vendor = get_vendor(request)
	category = Category.objects.get(pk=pk)
	food_items = FoodItem.objects.filter(category=category, vendor=vendor).order_by('-updated_at')
	
	context = {
			'food_items': food_items,
			'category': category,
	}

	return render(request, 'menu/food_item_by_category.html', context)


@user_passes_test(check_role_vendor)
def add_category(request):
	vendor = get_vendor(request)
	categories = Category.objects.filter(vendor=vendor).values('slug')
	
	slugList = []
	for category in categories:
		slugList.append(category.get('slug', None))
	
	if request.method == 'POST':
		category_form = CategoryForm(request.POST)
		if category_form.is_valid():
			category_name = category_form.cleaned_data.get('category_name')
			category = category_form.save(commit=False)
			category.vendor = get_vendor(request)
			slug = str(request.user.id) + "-" + slugify(category_name)
		
			if slug in slugList:
				messages.error(request, 'Please enter valid category.')
				return redirect('add_category')
			
			category.slug = slug
			category.save()

			messages.success(request, 'Category is created successfully.')
			return redirect('menu_builder')
		else:
			messages.error(request, 'Please enter valid data.')
			return redirect('add_category')
	else:
		category_form = CategoryForm()

	context = {
			'category_form': category_form,
	}

	return render(request, 'menu/add_category.html', context)


@user_passes_test(check_role_vendor)
def edit_category(request, pk):
	category = Category.objects.get(pk=pk)

	if request.method == 'POST':
		category_form = CategoryForm(request.POST, instance=category)

		if category_form.is_valid():
			category_name = category_form.cleaned_data.get('category_name')
			category = category_form.save(commit=False)
			# category.vendor = get_vendor(request)
			category.slug = slugify(category_name)
			category.save()

			messages.success(request, 'Category is updated successfully.')
			return redirect('menu_builder')
	else:
		category_form = CategoryForm(instance=category)

	context = {
			'category_form': category_form,
			'category': category,
	}

	return render(request, 'menu/edit_category.html', context)



@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
	category = get_object_or_404(Category, pk=pk)

	category.delete()

	messages.success(request, 'Category is deleted successfully.')
	return redirect('menu_builder')



@user_passes_test(check_role_vendor)
def add_food_item(request):
	if request.method == 'POST':
		food_item_form = FoodItemForm(request.POST, request.FILES)

		if food_item_form.is_valid():
			food_title = food_item_form.cleaned_data.get('food_title')
			foodItem = food_item_form.save(commit=False)
			vendor = get_vendor(request)
			foodItem.vendor = vendor
			foodItem.slug = str(vendor.id) + '-' +slugify(food_title)
			foodItem.save()

			messages.success(request, 'Food item added successfully.')
			return redirect('food_item_by_category', foodItem.category.id)
		else:
			messages.error(request, 'Some fields have incorrect data!')
			return redirect('add_food_item')

	else:
		food_item_form = FoodItemForm()
		food_item_form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

	context = {
			'food_item_form': food_item_form,
	}

	return render(request, 'menu/add_food_item.html', context)



@user_passes_test(check_role_vendor)
def edit_food_item(request, pk):
	foodItem = get_object_or_404(FoodItem, pk=pk)

	if request.method == 'POST':
		food_item_form = FoodItemForm(request.POST, request.FILES, instance=foodItem)

		if food_item_form.is_valid():
			food_title = food_item_form.cleaned_data.get('food_title')
			foodItem = food_item_form.save(commit=False)
			foodItem.vendor = get_vendor(request)
			foodItem.slug = slugify(food_title)
			foodItem.save()

			messages.success(request, 'Food item updated successfully.')
			return redirect('food_item_by_category', foodItem.category.id)
		else:
			messages.error(request, 'Some fields have incorrect data!')
			return redirect('add_food_item')

	else:
		food_item_form = FoodItemForm(instance=foodItem)
		food_item_form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

	context = {
			'food_item_form': food_item_form,
			'foodItem': foodItem,
	}

	return render(request, 'menu/edit_food_item.html', context)



@user_passes_test(check_role_vendor)
def delete_food_item(request, pk):
	foodItem = get_object_or_404(FoodItem, pk=pk)
	category = foodItem.category.id

	foodItem.delete()

	messages.success(request, 'Food item deleted successfully.')
	return redirect('food_item_by_category', category)