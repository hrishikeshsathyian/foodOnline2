from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages
# Create your views here.

def registeruser(request):
    if request.method == "POST" :
        print(request.POST) 
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            messages.success(request,'Account has been successfully created!')
            return redirect('registeruser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request,'accounts/registeruser.html',context)



def registervendor(request):
    if request.method == 'POST':
        #store the data and create the vendor
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.VENDOR
            user.set_password(password)
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,'Your vendor account has been registered successfully, please wait for admin approval')
            return redirect('registervendor')
        else:
            print(form.errors)
            print(vendor_form.errors)

    else:
        #render plain form normally
        form = UserForm()
        vendor_form = VendorForm()
    context = {
        'form':form,
        'vendor_form':vendor_form

    }
    return render(request,'accounts/registervendor.html',context)