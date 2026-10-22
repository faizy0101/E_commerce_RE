from django.contrib import admin


from ecom_app.models import seller, buyer, Login, product

# Register your models here.
admin.site.register(Login)
admin.site.register(seller)
admin.site.register(buyer)
admin.site.register(product)