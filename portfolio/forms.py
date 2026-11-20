from django import forms
from portfolio.models import Account, Asset


class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ["name"]