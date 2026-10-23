from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Login(AbstractUser):
    is_seller=models.BooleanField(default=False)
    is_buyer=models.BooleanField(default=False)


class buyer(models.Model):
    user=models.OneToOneField(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class seller(models.Model):
    user=models.OneToOneField(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    tax_number=models.CharField(max_length=100)
    def __str__(self):
        return self.name


class product(models.Model):
    seller=models.ForeignKey(seller,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_description=models.CharField(max_length=100)
    product_price=models.DecimalField(max_digits=10,decimal_places=2)
    product_category=models.CharField(max_length=100)
    product_quantity=models.IntegerField()
    product_image = models.ImageField(upload_to='products', default='products/default.jpg')

class cart(models.Model):
    product=models.ForeignKey(product,on_delete=models.DO_NOTHING)
    buyer=models.ForeignKey(buyer,on_delete=models.DO_NOTHING)
    quantity=models.PositiveIntegerField(default=1)

class order(models.Model):
    buyer=models.ForeignKey(buyer,on_delete=models.DO_NOTHING)
    products_ordered=models.ManyToManyField(product)
    total_amount=models.PositiveIntegerField()
    #shipping
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)








