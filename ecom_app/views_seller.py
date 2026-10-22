
from django.http import request
from django.shortcuts import render, redirect
from ecom_app.forms import sellerform, productform
from ecom_app.models import buyer, seller, product


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


def product_create(request):
    user_1 = request.user
    seller_data = seller.objects.get(user=user_1)
    if request.method == 'POST':
        form = productform(request.POST, request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.seller=seller_data
            obj.save()
            return redirect('product_add')
    else:
        form = productform()
    return render(request, 'seller/add_product.html', {'form': form })

def product_view(request):
    user=request.user
    seller_filter=seller.objects.get(user=user)
    products=product.objects.filter(seller=seller_filter)
    return render(request,'seller/product_view.html',{'products':products})


def product_update(request,id):
    current_product=product.objects.get(id=id)
    if request.method == 'POST':
        form=productform(request.POST,request.FILES,instance=current_product)
        if form.is_valid():
            form.save()
            return redirect('product_view')
    else:
        form=productform(instance=current_product)
    return render(request, 'seller/product_update.html',{'form':form})

def product_delete(request, id):
    current_product=product.objects.get(id=id)
    current_product.delete()
    return redirect('product_view')