from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

# Restrit the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied
# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registeruser(request):
    if request.user.is_authenticated:
        messages.error(request,"You are already logged in!")
        return redirect('myaccount')
    else:
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
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('myaccount')
    else:
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



def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('myaccount')
    else:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request,'You are now logged in')
                return redirect('myaccount')
            else:
                messages.error(request,"Invalid Login Credentials")
                return redirect('login')


    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out!')
    return redirect('login')

@login_required(login_url="login")
def myaccount(request):
    user=request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url="login")
@user_passes_test(check_role_customer)
def customerdashboard(request):
    return render(request,"accounts/customerdashboard.html")

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    return render(request,"accounts/vendordashboard.html")