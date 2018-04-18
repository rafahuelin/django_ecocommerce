from django.conf import settings
from django.db import models

from products.models import Product


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new(self, user=None):
        print("From new")
        print(user)
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                print("From is authenticated")
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)
