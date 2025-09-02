from celery import shared_task, group, chord
from django.core.cache import cache
from .utils.cache_keys import restaurant_status_key
from django.db import transaction
from celery import shared_task
from .models import Order
from .provider.services import update_order_status
from django.utils import timezone
import time

@shared_task
def process_restaurant_order(order_id, restaurant_id):

    key = restaurant_status_key(order_id, restaurant_id)
    cache.set(key, "processing", timeout=3600)


    cache.set(key, "done", timeout=3600)
    return {"order_id": order_id, "restaurant_id": restaurant_id, "status": "done"}

@shared_task
def start_delivery_task(order_id):

    from .provider.services import start_delivery_for_order
    with transaction.atomic():
        start_delivery_for_order(order_id)
    return {"order_id": order_id, "delivery_started": True}

@shared_task
def process_order_task(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    # меняем статус на "processing"
    order.status = "processing"
    order.save()

    # симуляция обработки
    import time
    time.sleep(5)  # задержка для теста

    # меняем статус на "ready for delivery"
    order.status = "ready_for_delivery"
    order.save()

@shared_task
def check_orders_status():
    orders = Order.objects.filter(status="processing")
    for order in orders:
        update_order_status(order.id)