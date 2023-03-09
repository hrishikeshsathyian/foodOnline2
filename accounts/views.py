from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from vendor.models import Vendor
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email, send_password_reset_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
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
                #send verification email 
                send_verification_email(request,user)
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
                # send activation email to the vendors email
                send_verification_email(request,user)
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

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Congratulations your account is activated")
        return redirect('myaccount')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('myaccount')

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
    vendor = Vendor.objects.get(user=request.user)
    context= {
    'vendor':vendor
    }
    return render(request,"accounts/vendordashboard.html",context)


def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            send_password_reset_email(request,user)
            messages.success(request,"Password reset link has been sent to the email address above. Do check Spam Folder if it does not show up")
            return redirect('login')
        else:
            messages.error(request,"Account does not exist")
            return redirect("forgot_password")
    return render(request,'accounts/forgot_password.html')
def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request,"Please reset your password")
        return redirect("reset_password")
    else:
        messages.error(request,"This link is expired")
        return redirect('myaccount')
    
def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,"Password Reset Successfully")
            return redirect('login')
        else:
            messages.error(request,"Passwords do not match")
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')
