from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from datetime import datetime


class Item(models.Model):
    image = models.ImageField(upload_to='images')
    name = models.CharField(max_length=40, default='item')
    discount_price = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(default=600)
    description = models.TextField(default='It is awesome')
    discount = models.BooleanField(default=False)
    slug = models.SlugField(default='test-item')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ecommerce:product", kwargs={
            'slug': self.slug,
            'pk': self.id
        })

    def get_add_to_cart_url(self):
        return reverse("ecommerce:add_to_cart", kwargs={
            'slug': self.slug,
            'pk': self.id
        })

    def get_remove_form_cart_url(self):
        return reverse("ecommerce:remove_from_cart", kwargs={
            'slug': self.slug,
            'pk':self.id
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"Quantity {self.quantity} of {self.item.name}"

    def total_item_price(self):
        return self.quantity * self.item.price

    def total_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_total_price(self):
        if self.item.discount_price:
            return self.total_discount_price()
        else:
            return self.total_item_price()

    def get_amount_saved(self):
        return self.total_item_price() - self.total_discount_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, blank=True, null=True)
    item = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(default=datetime.now())
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_final_price(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_total_price()
        return total


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)