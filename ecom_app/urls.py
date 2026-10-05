from django.urls import path

from ecom_app import views

urlpatterns=[
    path('',views.index,name='index'),
    path('base',views.admin_page, name='base'),
    path('login',views.login,name='login'),
]