def restaurant_status_key(order_id, restaurant_id):
    return f"order:{order_id}:restaurant:{restaurant_id}:status"

def delivery_status_key(order_id):
    return f"order:{order_id}:delivery:status"
