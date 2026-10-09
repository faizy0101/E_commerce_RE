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


