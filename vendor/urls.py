from django.urls import path, include
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('',AccountViews.vendordashboard,name='vendor'),
    path('vprofile/', views.vprofile,name='vprofile'),
    path('menubuilder/',views.menu_builder,name='menu_builder'),
    path('menubuilder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # category crud 
    path('menubuilder/category/add/', views.add_category , name = 'add_category'),
    path('menubuilder/category/edit/<int:pk>',views.edit_category,name='edit_category'),
    path('menubuilder/category/delete/<int:pk>',views.delete_category,name="delete_category"),
    #fooditem crud
    
    path('menubuilder/food/add',views.add_food,name='add_food'),
    path('menubuilder/food/edit/<int:pk>',views.edit_food,name='edit_food'),
    path('menubuilder/food/delete/<int:pk>',views.delete_food,name='delete_food'),
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/',views.add_opening_hours,name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>',views.remove_opening_hours,name='remove_opening_hours'),
    
    ] 