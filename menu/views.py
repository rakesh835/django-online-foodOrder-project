from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib import messages

from vendor.models import Vendor
from .models import Category, FoodItem
from vendor.utils import get_vendor
from .forms import CategoryForm

# Create your views here.


def menu_builder(request):
	vendor = get_vendor(request)
	print('vendor: ', vendor)
	categories = Category.objects.filter(vendor=vendor).order_by('-updated_at')
	print('categories: ', categories)
	context = {
			'categories': categories,
	}
	return render(request, 'menu/menu_builder.html', context)



def food_item_by_category(request, pk=None):
	vendor = get_vendor(request)
	category = Category.objects.get(pk=pk)
	food_items = FoodItem.objects.filter(category=category, vendor=vendor)
	
	context = {
			'food_items': food_items,
			'category': category,
	}

	return render(request, 'menu/food_item_by_category.html', context)



def add_category(request):
	if request.method == 'POST':
		category_form = CategoryForm(request.POST)
		if category_form.is_valid():
			category_name = category_form.cleaned_data.get('category_name')
			category = category_form.save(commit=False)
			category.vendor = get_vendor(request)
			category.slug = slugify(category_name)
			category.save()

			messages.success(request, 'Category is created successfully.')
			return redirect('menu_builder')
		else:
			print("errors: ", category_form)
			messages.error(request, 'Please enter valid data.')
			return redirect('add_category')
	else:
		category_form = CategoryForm()

	context = {
			'category_form': category_form,
	}

	return render(request, 'menu/add_category.html', context)



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



def delete_category(request, pk=None):
	category = get_object_or_404(Category, pk=pk)

	category.delete()

	messages.success(request, 'Category is deleted successfully.')
	return redirect('menu_builder')