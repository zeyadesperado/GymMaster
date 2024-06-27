from itertools import product
from django.db import models
from core.models import User


class Product(models.Model):
    name = models.CharField(max_length=50,
                             null=False,blank=False ,
                               verbose_name='Name')
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"
        ordering = ['name']


    def __str__(self) -> str:
        return f"{self.name}"
    
class Order(models.Model):

    ORDER_STATUS_CHOICES = [('Pending','pending'),
                            ('Done','done')]

    order_status = models.CharField( max_length=9 ,
                                     choices= ORDER_STATUS_CHOICES,
                                     default='Pending')
    total_quantity = models.IntegerField(default=0) 
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      default= 0.00,
                                      blank= True,
                                      null= True )
    user = models.ForeignKey( User,
                              on_delete = models.SET_NULL,
                              null = True,
                              blank = True,
                              related_name='orders')
    

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = 'orders'
        ordering = ['-id']
    
    def __str__(self) -> str:
        return f"Order: {self.id}  current status: {self.order_status}"

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='order_items' , null =True) 

    quantity = models.DecimalField( max_digits= 5 ,
                                    decimal_places=2,
                                    default= 1.0,
                                    null = False )
    class Meta:
        db_table = 'order_items'
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ['-id']


    def __str__(self):
        return f"{self.product.name}: {self.quantity}"