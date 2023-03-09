from django.shortcuts import render

# Create your views here.
def vprofile(request):
    context = {}
    return render(request,'vendor/vprofile.html',context)