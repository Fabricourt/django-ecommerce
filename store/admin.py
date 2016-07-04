from django.contrib import admin

from .models import Warehouse, Product, ProductPicture, Client, ContactInfo, Order

admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(ProductPicture)
admin.site.register(Client)
admin.site.register(ContactInfo)
admin.site.register(Order)

