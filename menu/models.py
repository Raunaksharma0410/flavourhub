from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Fooditems(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image =models.ImageField(upload_to='foods/',blank=True,null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    description = models.TextField()
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.name
