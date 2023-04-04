from .models import Cart, Tax
from menu.models import FoodItem

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items.exists():
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    
    print("cart_count -->: "+ str(cart_count))
    print(dict(cart_count=cart_count))
    return dict(cart_count=cart_count)

def get_cart_price(request):
    cart_price = 0
    tax_amount = 0
    total = 0
    tax_dict = {}
    try:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            cart_price += item.fooditem.price*item.quantity
        get_tax = Tax.objects.filter(is_active=True)
        print(get_tax)
        if get_tax.count() is not 0:
            for i in get_tax:
                tax_type = i.tax_type 
                tax_percentage = i.tax_percentage
                tax_amount = round((tax_percentage * cart_price)/100,2)
                tax_dict.update({tax_type:{tax_percentage:tax_amount}})
                total = cart_price + tax_amount
        else:
            total = cart_price
    except:
        print('t')
    print(cart_price)
    print(tax_amount)
    print(total)
    return dict(cart_price=cart_price,tax_amount=tax_amount,total=total,tax_dict=tax_dict)

