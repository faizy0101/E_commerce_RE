from django.db.models import Model
from django.shortcuts import render

from ecom_app.models import buyer


def profile_view(request):
    userdata=request.user
    buyer_user=buyer.objects.get(user=userdata)
    return render(request,'buyer/profile_view_buyer.html',{'buyer_user':buyer_user})
