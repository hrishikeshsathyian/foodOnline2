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
    path('menubuilder/category/delete/<int:pk>',views.delete_category,name="delete_category")
    ] 