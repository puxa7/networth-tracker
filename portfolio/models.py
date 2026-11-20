from django.db import models
from django.conf import settings

class Account(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"
    
class Asset(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=14, decimal_places=6)
    quantity = models.DecimalField(max_digits=14, decimal_places=6)
    currency = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"
    