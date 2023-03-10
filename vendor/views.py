from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.models import UserProfile 
from .models import Vendor
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor,check_role_customer
# Create your views here.


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