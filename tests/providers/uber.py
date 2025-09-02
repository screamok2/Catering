import os
import time
import json
import random
import requests
from datetime import datetime, timezone

BASE_URL = "http://web:8000"
ORDER_STATUSES = ["not_started", "cooking", "cooked", "delivery", "delivered"]
USERNAME = os.getenv("UBER_USER", "admin@mail.com")
PASSWORD = os.getenv("UBER_PASS", "admin")

def get_jwt_token():
    url = f"{BASE_URL}/api/token/"
    resp = requests.post(url, json={"email": USERNAME, "password": PASSWORD}, timeout=5)
    resp.raise_for_status()
    return resp.json()["access"]

def get_last_order_id(token):
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
        raise RuntimeError(f"{data}")

    if not orders:
        raise RuntimeError("❌ Нет заказов в базе")

    return orders[-1]["id"], orders[-1]["status"]



def wait_for_webhook():

    for attempt in range(20):  # пробуем до 20 раз
        try:
            resp = requests.get("http://web:8000/admin/login/", timeout=2)
            if resp.status_code < 500:  # web отвечает
                print("✅ Web is ok!")
                return
        except Exception as e:
            print(f"⏳ Web не готов")
        time.sleep(3)
    raise RuntimeError("❌ Web is dead")


def main():
    token = get_jwt_token()
    order_id, order_status= get_last_order_id(token)

    webhook_url = os.getenv("WEBHOOK_URL", f"{BASE_URL}/food/webhooks/uber/?order_id={order_id}")

    print(f"order_id={order_id}, webhook={webhook_url}")

    if  order_status == "delivered":
        print(f"order {order_id} already delivered")

    elif order_status != "delivered":

        for status in ORDER_STATUSES:
            payload = {"event": status}
            try:
                resp = requests.post(webhook_url, json=payload, timeout=5)
                print(f"➡️  Order {order_id}  {status}")
            except Exception as e:
                print("❌ Ошибка при отправке:", e)
            time.sleep(5)

        print("✅ Delivered")


if __name__ == "__main__":
    main()
