from django.db.models import Model
from django.shortcuts import render, redirect
from ecom_app.models import buyer, product, cart


def profile_view(request):
    userdata=request.user
    buyer_user=buyer.objects.get(user=userdata)
    return render(request,'buyer/profile_view_buyer.html',{'buyer_user':buyer_user})


def product_view_buyer(request):
    products = product.objects.all()
    return render(request, 'buyer/product_card_list.html', {'products': products})

def open_product(request,id):
    current_product=product.objects.get(id=id)
    return render(request,'buyer/open_product_page.html',{'current_product':current_product})

def Cart(request,id):
    user=request.user
    customer_filter=buyer.objects.get(user=user)
    product_filter=product.objects.get(id=id)
    obj = cart()
    obj.product = product_filter
    obj.buyer = customer_filter
    obj.save()
    return redirect('product_view_buyer')
    # data = cart.objects.create(product = product_filter,buyer = customer_filter)
    # data.save()

def Cart_view(request):
    user=request.user
    customer_filter=buyer.objects.get(user=user)
    products=cart.objects.filter(buyer=customer_filter)
    total=0
    for p in products:
        if p.quantity == 0:
           p.delete()
        else:
            total+=((p.product.product_price)*(p.quantity))


    return render(request, 'buyer/cart_page.html', {'products':products, 'total':total})

def product_delete_from_cart(request, id):
    current_product=cart.objects.get(id=id)
    current_product.delete()
    return redirect('Cart_view')

def increase_quantity(request,id):
    current_product=cart.objects.get(id=id)
    if current_product.quantity < current_product.product.product_quantity:
        current_product.quantity = current_product.quantity + 1
    else:
        current_product.quantity = current_product.quantity
    current_product.save()
    return redirect('Cart_view')

def decrease_quantity(request,id):
    current_product=cart.objects.get(id=id)
    current_product.quantity = current_product.quantity - 1
    current_product.save()
    print(current_product.quantity)
    return redirect('Cart_view')


def checkout(request,id):
    cart_data=cart.objects.get(id=id)
    print(cart_data)
    #ordered_items=cart.objects.filter(buyer=buyer_user)
    # total_price=0
    # for p in ordered_items:
    #     total_price+=((p.product.product_price) * (p.quantity))


    #return redirect('order_confirmation')









