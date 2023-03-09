from django.urls import path, include
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('',AccountViews.vendordashboard,name='vendor'),
    path('vprofile/', views.vprofile,name='vprofile'),
    ] 