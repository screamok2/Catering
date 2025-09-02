from django.conf import settings
from django.urls import reverse
from django.core.cache import cache
from ..utils.cache_keys import delivery_status_key
from .uber import UberClient
from django.utils import timezone
from food.models import Order
from django.core.cache import cache
import time

PROVIDER_MAP = {
    "uber": UberClient,

}

def get_provider_client(provider_name: str):
    cls = PROVIDER_MAP.get(provider_name.lower())
    if not cls:
        raise ValueError(f"Unknown provider: {provider_name}")
    return cls()

def build_webhook_url(request=None, order_id=None, provider_name="uber"):

    base = getattr(settings, "SITE_URL", None)
    path = reverse("provider-uber-webhook")  # см. urls ниже
    if base:
        return f"{base}{path}?order_id={order_id}"
    if request:
        return request.build_absolute_uri(f"{path}?order_id={order_id}")

    return f"http://web:8000{path}?order_id={order_id}"

def start_delivery_for_order(order_id: int):
    from ..models import Order
    order = Order.objects.select_for_update().get(pk=order_id)
    provider_name = (order.provider or "uber").lower()

    webhook_url = build_webhook_url(order_id=order.id, provider_name=provider_name)
    client = get_provider_client(provider_name)
    tracking_id = client.start_delivery(order_id=order.id, webhook_url=webhook_url)


    order.delivery_tracking_id = tracking_id
    order.delivery_status = "started"
    order.save(update_fields=["delivery_tracking_id", "delivery_status"])

    cache.set(delivery_status_key(order.id), "started", timeout=3600)

def update_order_status(order_id):
    order = Order.objects.get(id=order_id)
    restaurant_statuses = cache.get(f"order:{order_id}:restaurants", {})
    if not restaurant_statuses:
        return
    if all(status == "ready" for status in restaurant_statuses.values()):
        time.sleep(10)  # задержка перед сменой статуса
        order.status = "in_transit"
        order.updated_at = timezone.now()
        order.save()