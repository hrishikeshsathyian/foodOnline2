from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .context_processors import get_cart_counter, get_cart_price
from vendor.models import Vendor
from menu.models import Category,FoodItem
from marketplace.models import Cart
from django.db.models import Prefetch
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request,'marketplace/listings.html',context)


def vendor_detail(request,vendor_slug):
    vendor = Vendor.objects.get(vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
        'food',
        queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context ={
        'vendor':vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request,'marketplace/vendor_detail.html',context)


def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if user has already added that food to the cart 
                try:
                    chkCart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    # increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status':'Success','message':'Increase Cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'price':get_cart_price(request)})

                except:
                    chkCart = Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Added the food to the cart','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'price':get_cart_price(request)})

            except: 
                return JsonResponse({'status':'Failed','message':'This Food Does Not Exist'})
 
        else:
            return JsonResponse({'status':'Failed','message':'Invalid Request'})
    else:
        return JsonResponse({'status':'login_required','message':'Please log in to continue'})
    
def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')== 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    if chkCart.quantity >1 :
                        chkCart.quantity -= 1
                        chkCart.save()
                        return JsonResponse({'status':'Success','message':'Item qty reduced by 1','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'price':get_cart_price(request)})
                    elif chkCart.quantity == 1:
                        chkCart.delete()
                        return JsonResponse({'status':'Success','message':'Item removed from cart','cart_counter':get_cart_counter(request),'qty':'0','price':get_cart_price(request)})
                except:
                    return JsonResponse({'status':'item_not_in_cart','message':'The item is not in the cart yet'})

            except:
                return JsonResponse({'status':'Failed','message':'This Food Does Not Exist'})
    else:
        return JsonResponse({'status':'login_required','message':'Please log in to continue'})
    



def cart(request):
    
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items':cart_items
    }
    return render(request,'marketplace/cart.html',context)


def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')== 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Cart Item has been removed','cart_counter':get_cart_counter(request),'price':get_cart_price(request)})
            except:
                return  JsonResponse({'status':'Failed','message':'Cart Item does not Exist'})     
        else:
            return JsonResponse({'status':'Failed','message':'Invalid Request'})


def search(request):
    
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']

    # get vendor ids that have the food item that the user is looking for 
    fetch_vendor_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword,is_available=True).values_list('vendor',flat=True)
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendor_by_fooditems) | Q(vendor_name__icontains=keyword,is_approved=True,user__is_active=True))

    if latitude and longitude and radius:
        pnt = GEOSGeometry('POINT(%s %s)' %(longitude,latitude))
        print(pnt)
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendor_by_fooditems) | Q(vendor_name__icontains=keyword,is_approved=True,user__is_active=True),user_profile__location__distance_lte=(pnt, D(km=radius)) ).annotate(distance=Distance('user_profile__location',pnt)).order_by('distance')
        
        for v in vendors:
            v.kms = round(v.distance.km,3)
        print(vendors)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
        'source_location': address,
    }
    
    return render(request,'marketplace/listings.html',context)