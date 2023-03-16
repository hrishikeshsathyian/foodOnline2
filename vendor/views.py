from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.models import UserProfile 
from .models import Vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor,check_role_customer
from django.template.defaultfilters import slugify
# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor 

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)


    if request.method == "POST":
        profile_form = UserProfileForm(request.POST,request.FILES,instance = profile)
        vendor_form = VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,"Your restaraunt profile has been updated")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:

        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'vendor':vendor,
        'profile': profile,
        'profile_form': profile_form,
        'vendor_form': vendor_form,
    }
    return render(request,'vendor/vprofile.html',context)



@login_required(login_url="login")
@user_passes_test(check_role_vendor)

def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'vendor':vendor,
        'categories':categories,
    }
    return render(request,'vendor/menu_builder.html',context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
    print(fooditems)
    context= {
        'cat':category,
        'fooditems': fooditems,
    }
    return render(request,'vendor/fooditems_by_category.html',context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def add_category(request):

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request,'New Category Successfully added')
            return redirect('menu_builder')
        else:
            print(form.errors)
            messages.error(request,'Category Not saved')
    else:
        form = CategoryForm()
        
    

    context = {
        'form': form
    }
    return render(request,'vendor/add_category.html',context)






def edit_category(request,pk):
    category = Category.objects.get(pk=pk)
    if request.POST:
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            title = form.cleaned_data['category_name']
            category.slug = slugify(title)
            category = form.save()
            messages.success(request,"Updated Succesfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
      'category':category,
      'form': form,
    }
    return render(request,'vendor/edit_category.html',context)


def delete_category(request,pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    messages.success(request,"Category has been successfully deleted")
    return redirect('menu_builder')


def add_food(request):

    if request.POST:
        form = FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            food.save()
            messages.success(request,'Food Item Added Successfully')
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        # modify this form
        form.fields['category'].queryset.filter(vendor=get_vendor(request))
    context = {
        'form':form,
    }
    return render(request,'vendor/add_food.html',context)




def edit_food(request,pk):
    food = FoodItem.objects.get(pk=pk)
    if request.POST:
        form = FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food.slug  =slugify(foodtitle)
            food = form.save()
            messages.success(request,"Updated Succesfully")
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset.filter(vendor=get_vendor(request))

    context = {
      'food':food,
      'form': form,
    }
    return render(request,'vendor/edit_food.html',context)

def delete_food(request,pk):
    food = FoodItem.objects.get(pk=pk)
    food.delete()
    messages.success(request,'Food Item has successfully been deleted')
    return redirect('fooditems_by_category',food.category.id)
