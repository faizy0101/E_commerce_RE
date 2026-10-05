from urllib import request

from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_page(request):
    return render(request,'base.html')

def login(request):
    return render(request,'login.html')