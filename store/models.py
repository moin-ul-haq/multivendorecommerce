from django.db import models
from accounts.models import User
from django.utils.text import slugify


class Store(models.Model):
    name=models.CharField(max_length=30)
    slug=models.SlugField(null=True,blank=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='store')

    def save(self,*args,**kwargs):
        if not self.slug:
            base_slug=slugify(self.name)
            slug=base_slug
            counter=1
            while Store.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug=f'{base_slug}-{counter}'
                counter+=1
            self.slug=slug
        super().save(*args,**kwargs)



class Catagory(models.Model):
    name=models.CharField(max_length=30)
    store=models.ForeignKey(Store,on_delete=models.CASCADE,related_name='catagory')
    slug=models.SlugField()

    def save(self,*args,**kwargs):
        if not self.slug:
            base_slug=slugify(self.name)
            slug=base_slug
            counter=1
            while Catagory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug=f'{base_slug}-{counter}'
                counter+=1
            self.slug=slug
        super().save(*args,**kwargs)



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
            base_slug=slugify(self.name)
            slug=base_slug
            counter=1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug=f'{base_slug}-{counter}'
                counter+=1
            self.slug=slug
        super().save(*args,**kwargs)


class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    rating=models.IntegerField()
    review=models.TextField(blank=True)

    class Meta:
        unique_together=('product','user')

    def __str__(self):
        return self.user.name+" "+self.product.name