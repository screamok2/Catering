from django.contrib import admin
from django import forms
from django.urls import path
from .views import import_dishes
from django.template.response import TemplateResponse

from .models import Dish, Order, OrderItem, Restaurant


admin.site.register (Restaurant)
admin.site.register (OrderItem)

@admin.register(Dish)
class DishAdmin (admin.ModelAdmin):
    change_list_template = "admin/food/dish/change_list.html"
    list_display = ("name","id", "price", "restaurant")
    search_fields = ("name",)
    list_filter = ("name","restaurant")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-dishes/", import_dishes, name="import_dishes"),
        ]
        return custom_urls + urls


class DishOrderItemInline (admin.TabularInline):
    model = OrderItem

@admin.register( Order )
class OrderAdmin (admin.ModelAdmin):
    list_display = ('__str__', "id", "delivery_provider","status")
    inlines = ( DishOrderItemInline, )

class CSVImportForm(forms.Form):
    file = forms.FileField()