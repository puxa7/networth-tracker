from django.contrib import admin
from .models import Account, Asset


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ["name", "ticker", "price", "quantity", "currency", "account"]
