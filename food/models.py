from django.db import models
from django.conf import settings

import enum

class OrderStatus(enum.StrEnum):
    NOT_STARTED = enum.auto()
    WAITING = enum.auto()
    COOKING = enum.auto()
    COOKING_REJECTED = enum.auto()
    COOKED = enum.auto()

    DELIVERY_LOOKUP = enum.auto()
    DELIVERY = enum.auto()
    DELIVERED = enum.auto()
    NOT_DELIVERED = enum.auto()

    CANCELLED_BY_CUSTOMER = enum.auto()
    CANCELLED_BY_MANAGER = enum.auto()
    CANCELLED_BY_ADMIN = enum.auto()
    CANCELLED_BY_RESTAURANT = enum.auto()
    CANCELLED_BY_DRIVER = enum.auto()
    FAILED = enum.auto()

    @classmethod
    def choices(cls):
        results = []

        for el in cls:
            _el = (el.value, el.name.lower().capitalize())
            results.append(_el)

        return results

class Restaurant(models.Model):
    class Meta:
        db_table = "restaurant"
    name = models.CharField(max_length=255, null=False)
    address = models.TextField(null=False)

    def __str__(self):
        return f"{self.name}"

class Dish(models.Model):
    class Meta:
        db_table = "dishes"

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    restaurant = models.ForeignKey(
        "Restaurant",
        on_delete = models.CASCADE
    )
    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    class Meta:
        db_table = "orders"

    status = models.CharField(max_length=50, choices=OrderStatus.choices,
                              default=OrderStatus.NOT_STARTED)

    delivery_provider = models.CharField(max_length=20, null=True)
    eta = models.DateField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return f"{self.pk}  {self.status} for {self.user}"

class OrderItem(models.Model):
    class Meta:
        db_table = "order_items"

    quantity = models.SmallIntegerField()
    dish = models.ForeignKey("Dish", on_delete = models.CASCADE)
    order = models.ForeignKey("Order", on_delete = models.CASCADE )

    def __str__(self):
        return f"{self.order.pk}  {self.dish.name}  {self.quantity}"