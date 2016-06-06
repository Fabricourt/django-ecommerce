from django.db import models


# Store supply
# Warehouses where products are stored (stock)
class Warehouse(models.Model):
    description = models.CharField(max_length=200)


# Product sold on the store
class Product(models.Model):
    description = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date published')


# Pictures describing a product
class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    picture_url = models.URLField()


# Stock of product in warehouse
class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_count = models.IntegerField(default=0)


# Client activity
# Clients of the store
class Client(models.Model):
    email = models.EmailField()
    billing_adress = models.CharField(max_length=200)
    shipping_adress = models.CharField(max_length=200)
    creation_date = models.DateTimeField()


# Client Orders
class Order(models.Model):
    client = models.ForeignKey(Client)
    creation_date = models.DateTimeField()
    shipping_adress = models.CharField(max_length=200)


# Stock of product in warehouse
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    product_count = models.IntegerField(default=0)
