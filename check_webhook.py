import requests

resp = requests.get("http://web:8000/food/orders/all")
print(resp.status_code)
print(resp.text[:200])
