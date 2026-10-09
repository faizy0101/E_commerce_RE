from django.shortcuts import render, redirect

from ecom_app.forms import buyerform
from ecom_app.models import buyer


def view_customers(request):
    customers=buyer.objects.all()
    return render(request,'admin/customers.html',{'customers':customers})

def update_customers(request,id):
    customers=buyer.objects.get(id=id)
    if request.method=="POST":
        form=buyerform(request.POST,instance=customers)
        if form.is_valid():
            form.save()
            return redirect('view_customers')
    else:
        form=buyerform(instance=customers)
    return render(request,'admin/customers.html',{'form':form})

def delete_customers(request,id):
    customers=buyer.objects.get(id=id)
    customers.delete()
    return render('admin/customers.html')

