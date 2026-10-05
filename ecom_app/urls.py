from django.urls import path

from ecom_app import views

urlpatterns=[
    path('',views.index,name='index'),
    path('base',views.admin_page, name='base'),
    path('login',views.login,name='login'),
    path('user_add',views.user_add,name='user_add'),
    path('customer_add',views.customer_add,name='customer_add'),
]