from django.contrib import admin
from shop import models

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_status', 'total_quantity', 'total_price', 'user']
    list_filter = ['order_status', 'user']
    search_fields = ['user__email', 'id']

admin.site.register(models.Order, OrderAdmin)