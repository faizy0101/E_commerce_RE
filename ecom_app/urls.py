from django.urls import path

from ecom_app import views, views_admin

urlpatterns=[
    path('',views.index,name='index'),
    path('base',views.admin_page, name='base'),
    path('login',views.login_view,name='login'),
    path('user_add',views.user_add,name='user_add'),
    path('customer_add',views.customer_add,name='customer_add'),
    path('seller_page',views.seller_page,name='seller_page'),
    path('buyer_page',views.buyer_page,name='buyer_page'),
    path('admin_page', views.admin_page, name='admin_page'),


#     admin
    path('view_customers', views_admin.view_customers, name='view_customers'),
    path('update_customers/<int:id>',views_admin.update_customers, name='update_customers'),
    path('delete_customers/<int:id>', views_admin.delete_customers, name='delete_customers')


#     customer


#     seller
]