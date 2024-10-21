import uuid

from django.db import models


class Promotion(models.Model):
    description = models.TextField()
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    pass


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default=uuid.uuid1, editable=False)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion)
    pass


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,
                                  choices=MEMBERSHIP_CHOICES,
                                  default=MEMBERSHIP_BRONZE)
    pass


class Order(models.Model):
    PENDING = 'P'
    COMPLETED = 'C'
    FAILED = 'F'
    PAYMENT_STATUS = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=255,
                                      choices=PAYMENT_STATUS,
                                      default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    pass


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pass


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    pass


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    pass


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
