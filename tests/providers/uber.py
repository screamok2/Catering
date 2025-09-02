import os
import time
import random
import requests

# Настройки
BASE_URL = os.getenv("WEB_BASE_URL", "https://catering-v45p.onrender.com")
ORDER_STATUSES = ["not_started", "cooking", "cooked", "delivery", "delivered"]
USERNAME = os.getenv("UBER_USER", "admin@mail.com")
PASSWORD = os.getenv("UBER_PASS", "admin")


def wait_for_service():
    for attempt in range(20):
        try:
            resp = requests.get(f"{BASE_URL}/admin/login/", timeout=5)
            if resp.status_code < 500:
                return True
        except:
            pass
        time.sleep(3)
    raise RuntimeError("❌ Service not ready")



def get_jwt_token():
    """Получаем JWT токен для авторизации"""
    url = f"{BASE_URL}/api/token/"
    resp = requests.post(url, json={"email": USERNAME, "password": PASSWORD}, timeout=5)
    resp.raise_for_status()
    return resp.json()["access"]


def get_last_order(token):
    """Получаем последний заказ"""
    url = f"{BASE_URL}/food/orders/all/"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, dict) and "results" in data:
        orders = data["results"]
    elif isinstance(data, list):
        orders = data
    else:
        raise RuntimeError(f"Unexpected response: {data}")

    if not orders:
        raise RuntimeError("❌ No orders in database")

    return orders[-1]["id"], orders[-1]["status"]


def main():
    # Ждём пока веб-сервис доступен
    wait_for_service(f"{BASE_URL}/admin/login/")

    token = get_jwt_token()
    order_id, order_status = get_last_order(token)
    webhook_url = f"{BASE_URL}/food/webhooks/uber/?order_id={order_id}"

    print(f"Using order_id={order_id}, webhook={webhook_url}")

    if order_status == "delivered":
        print(f"Order {order_id} already delivered")
        return

    # Последовательно отправляем статусы заказа
    for status in ORDER_STATUSES:
        payload = {"event": status}

        # Пока заказ не "delivered", симулируем координаты для delivery
        if status == "delivery":
            for _ in range(5):
                payload.update({
                    "lat": 55.7512 + (random.random() - 0.5) * 0.01,
                    "lng": 37.6184 + (random.random() - 0.5) * 0.01,
                })
                try:
                    resp = requests.post(webhook_url, json=payload, timeout=5)
                    print(f"➡️ Delivery coords sent → {resp.status_code}, {resp.text}")
                except Exception as e:
                    print("❌ Error sending coordinates:", e)
                time.sleep(5)
            continue

        try:
            resp = requests.post(webhook_url, json=payload, timeout=5)
            print(f"➡️ Order {order_id} {status} → {resp.status_code}, {resp.text}")
        except Exception as e:
            print("❌ Error sending status:", e)
        time.sleep(5)

    print("✅ All statuses sent!")


if __name__ == "__main__":
    main()
