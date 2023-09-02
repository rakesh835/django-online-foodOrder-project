from django.urls import path

from .views import (menu_builder, food_item_by_category, add_category, edit_category,
                    delete_category, add_food_item, edit_food_item, delete_food_item
    )



urlpatterns = [
    path('menu-builder/', menu_builder, name='menu_builder'),
    path('food_item_by_category/<int:pk>/', food_item_by_category, name='food_item_by_category'),
    
    # category builder
    path('category/add/', add_category, name='add_category'),
    path('category/edit/<int:pk>/', edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', delete_category, name='delete_category'),

    # food item builder
    path('food_item/add/', add_food_item, name='add_food_item'),
    path('food_item/edit/<int:pk>/', edit_food_item, name='edit_food_item'),
    path('food_item/delete/<int:pk>/', delete_food_item, name='delete_food_item'),
    
] 