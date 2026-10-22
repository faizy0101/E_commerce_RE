from django.urls import path

from ecom_app import views, views_admin, views_buyer, views_seller

urlpatterns=[
    path('',views.index,name='index'),
    path('base',views.admin_page, name='base'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('user_add',views.user_add,name='user_add'),
    path('customer_add',views.customer_add,name='customer_add'),
    path('seller_page',views.seller_page,name='seller_page'),
    path('buyer_page',views.buyer_page,name='buyer_page'),
    path('admin_page', views.admin_page, name='admin_page'),


#     admin
    path('view_customers', views_admin.view_customers, name='view_customers'),
    path('update_customers/<int:id>',views_admin.update_customers, name='update_customers'),
    path('delete_customers/<int:id>', views_admin.delete_customers, name='delete_customers'),


#     customer
    path('profile_buyer',views_buyer.profile_view, name='profile_buyer'),
    path('product_view_buyer',views_buyer.product_view_buyer, name='product_view_buyer'),
    path('open_product/<int:id>',views_buyer.open_product,name='open_product'),
    path('cart/<int:id>',views_buyer.Cart,name='cart'),
    path('Cart_view',views_buyer.Cart_view, name='Cart_view'),
    path('increase_quantity/<int:id>',views_buyer.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:id>',views_buyer.decrease_quantity, name='decrease_quantity'),
    path('checkout/<int:id>',views_buyer.checkout, name='checkout'),


#     seller
    path('profile_seller',views_seller.profile_view, name='profile_seller'),
    path('update_seller_profile/<int:id>',views_seller.update_seller_profile, name='update_seller_profile'),
    path('product_add',views_seller.product_create, name='product_add'),
    path('product_view',views_seller.product_view, name='product_view'),
    path('product_update/<int:id>',views_seller.product_update, name='product_update'),
    path('product_delete/<int:id>',views_seller.product_delete, name='product_delete'),

]