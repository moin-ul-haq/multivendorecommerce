from django.db import models
from store.models import Product
from accounts.models import User

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    is_active=models.BooleanField(default=True)


    def get_total(self):
        total_price=0
        for item in self.cartitem.all():
            total_price+=item.get_sub_total()
        return total_price
    
    def get_items_count(self):
        count=0
        for i in self.cartitem.all():
            count+=1
        return count
    
    def is_empty(self):
        cart=self.cartitem.all()
        if cart:
            return False
        return True
    
    def clear(self):
        for item in self.cartitem.all():
            item.delete()
    def __str__(self):
        return f"{self.user.name}'s Cart"




class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cartitem')
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartitem')
    quantity=models.IntegerField()
    unit_price=models.DecimalField(decimal_places=3,max_digits=12)


    def get_sub_total(self):
        return self.unit_price * self.quantity
    
    def stock_available(self):
        if self.quantity <= self.product.stock:
            return True
        return False
    def __str__(self):
        return self.cart.user.name+" "+self.product.name