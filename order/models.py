from django.db import models
from accounts.models import User
from store.models import Product


class Order(models.Model):
    status_choices=[
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    ]
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='order')
    status=models.CharField(choices=status_choices,default='pending')
    total_amount=models.DecimalField(max_digits=12,decimal_places=2)
    shipping=models.JSONField()


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
    quantity=models.IntegerField()
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    vendor_comission=models.DecimalField(max_digits=10, decimal_places=2)
    product_name=models.CharField(max_length=255)

    def __str__(self):
        return self.order.user.name + " "+self.product.name+" ------ "+f"({str(self.quantity)})"
