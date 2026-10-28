from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from ecom_app.forms import OrderForm
from ecom_app.models import buyer, product, cart, OrderItem


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
    user = request.user
    customer_filter = get_object_or_404(buyer, user=user)
    cart.objects.filter(buyer=customer_filter, quantity=0).delete()
    products = cart.objects.filter(buyer=customer_filter).select_related('product')
    total = sum((p.product.product_price * p.quantity) for p in products)

    return render(request, 'buyer/cart_page.html', {'products': products, 'total': total})

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
    user = request.user
    customer_filter = get_object_or_404(buyer, user=user)
    ordered_items = cart.objects.filter(buyer=customer_filter).select_related('product')

    if not ordered_items.exists():
        return redirect('Cart_view')

    total_price = sum((item.product.product_price * item.quantity) for item in ordered_items)


    for item in ordered_items:
        item.subtotal = item.product.product_price * item.quantity

    if request.method == "POST":

        order_data = OrderForm(request.POST)
        if order_data.is_valid():
            new_order = order_data.save(commit=False)
            new_order.buyer = customer_filter
            new_order.total_amount = total_price
            new_order.save()

            for item in ordered_items:

                OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.product_price,
                )
                item.product.product_quantity = F('product_quantity') - item.quantity
                item.product.save()

            ordered_items.delete()

            return redirect('order_placed')
    else:
        order_data = OrderForm()

    return render(request, 'buyer/checkout.html', {
        'form': order_data,
        'buyer_user': customer_filter,
        'total': total_price,
        'cart_items': ordered_items,
    })

def order_placed(request):
    return render(request, 'buyer/order_placed.html')








