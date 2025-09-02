from django.urls import path
from .views import DishesListView, DishCreateView, OrderCreateView, OrdersListView, import_dishes, uber_webhook

urlpatterns = [
    path("dishes/", DishesListView.as_view(), name="dish-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    path("orders/all/", OrdersListView.as_view(), name="order-list"),
    path("import-dishes/", import_dishes, name="import_dishes"),
    path("webhooks/uber/", uber_webhook, name="provider-uber-webhook"),
]
