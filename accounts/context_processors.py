from vendor.models import Vendor


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        # in the event that there is no vendor to collect data from
        vendor = None
    return dict(vendor=vendor)