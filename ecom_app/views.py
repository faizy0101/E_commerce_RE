from urllib import request

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from ecom_app.forms import loginform, sellerform, buyerform


# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_page(request):
    return render(request,'base.html')

def login(request):
    return render(request,'login.html')
#
# def user_page(request):
#     form=UserCreationForm()
#     return render(request,'user.html',{'form':form})

def user_add(request):
    form1=loginform()
    form2=sellerform()
    if request.method=="POST":
        form1=loginform(request.POST)
        form2=sellerform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user_data=form1.save(commit=False)
            user_data.is_seller=True
            user_data.save()
            user1=form2.save(commit=False)
            user1.user=user_data
            user1.save()
            return redirect('login')
    return render(request,'user_add.html',{'form1':form1,'form2':form2})

def customer_add(request):
    form1=loginform()
    form2=buyerform()
    if request.method=="POST":
        form1=loginform(request.POST)
        form2=buyerform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user_data=form1.save(commit=False)
            user_data.is_buyer=True
            user_data.save()
            user1=form2.save(commit=False)
            user1.user=user_data
            user1.save()
            return redirect('login')
    return render(request,'customer_add.html',{'form1':form1,'form2':form2})
