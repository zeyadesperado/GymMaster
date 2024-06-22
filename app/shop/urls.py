from django.urls import (
    path,
    include,
    )

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('OrderItems', views.OrderItemViewSet)
router.register('Orders', views.OrderViewSet)
router.register('Products', views.ProductViewSet)

app_name = 'shop'

urlpatterns = [
    path('', include(router.urls)),
]
