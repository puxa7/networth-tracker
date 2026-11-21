from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm, AssetForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Asset
from decimal import Decimal
import yfinance as yf


@login_required
def home_view(request):
    accounts = Account.objects.filter(user=request.user).prefetch_related("asset_set")
    
    net_worth = Decimal("0.00")
    for account in accounts:
        net_worth += account.total_value
    
    return render(request, "portfolio/home.html", {
        "accounts": accounts,
        "net_worth": net_worth,
    })


@login_required
def account_detail_view(request, pk):
    account = get_object_or_404(Account, id=pk, user=request.user)
    assets = account.asset_set.all()

    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.account = account
            asset.save()
            return redirect("account_detail", pk=account.id)
    else:
        form = AssetForm()

    return render(request, "portfolio/account_detail.html", {
        "account": account,
        "assets": assets,
        "form": form,
    })


@login_required
def add_account_view(request):

    if request.method == "POST":
        form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("home")
    else:
        form = AccountForm()

    return render(request, "portfolio/add_account.html", {"form": form})


@login_required
@require_POST
def refresh_prices_view(request):
    assets = Asset.objects.filter(account__user=request.user)
    
    for asset in assets:
        try:
            ticker_data = yf.Ticker(asset.ticker)
            latest_price = ticker_data.fast_info["last_price"]
            if latest_price:
                asset.price = Decimal(str(round(latest_price, 6)))
                asset.save()
        except Exception:
            continue
    
    return redirect("home")


@login_required
@require_POST
def edit_account_view(request, pk):
    account = get_object_or_404(Account, id=pk, user=request.user)
    form = AccountForm(request.POST, instance=account)
    if form.is_valid():
        form.save()
    return redirect("account_detail", pk=account.id)