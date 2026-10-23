from django.db.models import Model
from django.shortcuts import render, redirect

from ecom_app.forms import OrderForm
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


def checkout(request):
    form = OrderForm()
    user = request.user
    customer_filter = buyer.objects.get(user=user)
    ordered_items = cart.objects.filter(buyer=customer_filter)
    total_price = 0
    for p in ordered_items:
        if p.quantity == 0:
            p.delete()
            continue
        total_price += ((p.product.product_price) * (p.quantity))
    #clear cart after checkout
    # ordered_items.delete()

    if request.method == "POST":
        order_data = OrderForm(request.POST)
        if order_data.is_valid():
            print("ok1")
            user_data=order_data.save(commit=False)
            user_data.buyer=customer_filter
            user_data.total_amount = total_price
            print("ok2")


            user_data.save()

            user_data.save()

            print("Order ID:", user_data.id)
            print("Ordered items:", list(ordered_items))

            products = [item.product for item in ordered_items]
            print("Products to save:", products)

            user_data.products_ordered.add(*products)

            print("Saved products:", list(user_data.products_ordered.all()))


    return render(request, 'buyer/checkout.html', {'form':form,'buyer_user': customer_filter, 'total': total_price})









