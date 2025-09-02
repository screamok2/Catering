import os
import requests

class UberClient:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or os.getenv("UBER_BASE_URL", "http://uber:5002")
        self.api_key = api_key or os.getenv("UBER_API_KEY", "test-key")

    def start_delivery(self, order_id: int, webhook_url: str) -> str:

        payload = {"order_id": order_id, "webhook_url": webhook_url}
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            resp = requests.post(f"{self.base_url}/start", json=payload, headers=headers, timeout=5)
            resp.raise_for_status()
            data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            return data.get("tracking_id", f"uber-{order_id}")
        except Exception:

            return f"uber-{order_id}"