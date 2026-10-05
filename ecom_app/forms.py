from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import (forms)

from ecom_app.models import Login, seller, buyer

#
# class userform(forms.ModelForm):
#     class Meta:
#         model = User
#         fields= '__all__'

class loginform(UserCreationForm):
    class Meta:
        model = Login
        fields= ('username','password1','password2')

class buyerform(forms.ModelForm):
    class Meta:
        model=buyer
        fields= '__all__'
        exclude=("user",)


class sellerform(forms.ModelForm):
    class Meta:
        model=seller
        fields= '__all__'
        exclude=("user",)
