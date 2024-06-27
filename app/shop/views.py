from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'name']



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('order_items')
    serializer_class = OrderSerializer

    
    def update(self, request, *args, **kwargs):
        # Retrieve the Order object
        order = self.get_object()

        order_items_data = request.data.get('order_items', None)
        
        if order_items_data:
            for item_data in order_items_data:
             
                existing_order_item = OrderItem.objects.filter(order=order).first()

                if existing_order_item:

                    existing_order_item.quantity += item_data['quantity']
                    existing_order_item.save()
                else:

                    OrderItem.objects.create(order=order, quantity=item_data['quantity'])
            
        
        return super().update(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

