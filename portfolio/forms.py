from django import forms
from portfolio.models import Account, Asset


class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ["name"]
        
        
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "ticker", "price", "quantity", "currency"]