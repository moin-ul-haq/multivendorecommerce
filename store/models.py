from django.db import models
from accounts.models import User
from django.utils.text import slugify


class Store(models.Model):
    name=models.CharField(max_length=30)
    slug=models.SlugField()
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='store')



class Catagory(models.Model):
    name=models.CharField(max_length=30)
    store=models.ForeignKey(Store,on_delete=models.CASCADE,related_name='catagory')
    slug=models.SlugField()



class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    # image=models.ImageField(upload_to='media',null=True,blank=True)
    stock=models.IntegerField()
    store=models.ForeignKey(Store,on_delete=models.CASCADE,related_name='product')
    catagory=models.ForeignKey(Catagory,on_delete=models.SET_NULL,related_name='product',null=True)
    slug=models.SlugField(null=True,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)