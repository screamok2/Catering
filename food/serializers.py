from rest_framework import serializers
from .models import Dish, Order, OrderItem, Restaurant


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("id", "name", "price", "restaurant")


class DishGroupedSerializer(serializers.ModelSerializer):
    dishes = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ("id", "name", "dishes")

    def get_dishes(self, obj):
        dishes = obj.dish_set.all()
        return DishSerializer(dishes, many=True).data


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("dish", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ("id", "eta", "delivery_provider", "items", "status")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(user=self.context["request"].user, **validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order
