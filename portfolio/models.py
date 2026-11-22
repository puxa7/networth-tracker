from django.db import models
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import User


class UserProfile(models.Model):
    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ("PLN", "PLN"),
        ("EUR", "EUR"),
        ("GBP", "GBP"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")
    
    def __str__(self):
        return f"{self.user.username} ({self.display_currency})"
    


class Account(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"
    
    @property
    def total_value(self):
        total = Decimal("0.00")
        for asset in self.asset_set.all():
            total += asset.total_value
        return total
    
    
    
class Asset(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=14, decimal_places=6)
    quantity = models.DecimalField(max_digits=14, decimal_places=6)
    currency = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"
    
    @property
    def total_value(self):
        return self.quantity * self.price