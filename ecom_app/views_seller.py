from django.shortcuts import render, redirect

from ecom_app.forms import sellerform
from ecom_app.models import buyer, seller


def profile_view(request):
    userdata=request.user
    seller_user=seller.objects.get(user=userdata)
    return render(request,'seller/profile_view_seller.html',{'seller_user':seller_user})


def update_seller_profile(request,id):
    seller_user=seller.objects.get(id=id)
    if request.method=="POST":
        form=sellerform(request.POST,instance=seller_user)
        if form.is_valid():
            form.save()
            return redirect('profile_seller')
    else:
        form=sellerform(instance=seller_user)
    return render(request,'seller/update_seller_profile.html',{'form':form})
