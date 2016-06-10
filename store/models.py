from django.db import models


# Store supply
# Warehouses where products are stored (stock)
class Warehouse(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Product sold on the store
class Product(models.Model):
    reference = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.FloatField()
    weight = models.FloatField()
    tax_class_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
    categories = models.CharField(max_length=200)
    product_online = models.BooleanField(default=False)
    creation_date = models.DateTimeField()

    def __str__(self):
        return self.name


# Pictures describing a product
class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    picture_url = models.URLField()
    picture_type = models.CharField(max_length=200)


# Stock of product in warehouse
class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'warehouse',)


# Client activity
# Clients of the store
class Client(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    creation_date = models.DateTimeField()
    gender = models.NullBooleanField()
    password_hash = models.CharField(max_length=64)
    password_salt = models.CharField(max_length=32)

    def __str__(self):
        return self.email


# Client contact info
class ContactInfo(models.Model):
    client = models.ForeignKey(Client)
    city = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    country_id = models.CharField(max_length=200)
    fax = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    vat_id = models.CharField(max_length=200)
    address_default_billing = models.BooleanField(default=False)
    address_default_shipping = models.BooleanField(default=False)

    def __str__(self):
        return "%s's address" % self.client


# Client Orders
class Order(models.Model):
    client = models.ForeignKey(Client)
    creation_date = models.DateTimeField()
    shipping_adress = models.ForeignKey(ContactInfo)

    def __str__(self):
        return "%s's order - %s" % (self.client, self.creation_date)


# Stock of product in warehouse
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    product_count = models.IntegerField(default=0)
