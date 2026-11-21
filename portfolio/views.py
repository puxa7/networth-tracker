from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm, AssetForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Asset
from decimal import Decimal, InvalidOperation
import yfinance as yf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout



def _update_assets_prices(assets):
    for asset in assets:
        try:
            ticker_data = yf.Ticker(asset.ticker)
            latest_price = ticker_data.fast_info["last_price"]
            if latest_price:
                asset.price = Decimal(str(round(latest_price, 6)))
                asset.save()
        except Exception:
            continue

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
    _update_assets_prices(assets)
    return redirect("home")


@login_required
@require_POST
def edit_account_view(request, pk):
    account = get_object_or_404(Account, id=pk, user=request.user)
    form = AccountForm(request.POST, instance=account)
    if form.is_valid():
        form.save()
    return redirect("account_detail", pk=account.id)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
        
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
            form = UserCreationForm()
            
    return render(request, "portfolio/register.html", {"form": form})


@login_required
def settings_view(request):
    return render(request, "portfolio/settings.html")


@login_required
@require_POST
def delete_user_view(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect("login")


@login_required
@require_POST
def delete_account_view(request, pk):
    account = get_object_or_404(Account, id=pk, user=request.user)
    account.delete()
    return redirect("home")


@login_required
@require_POST
def edit_asset_quantity_view(request, pk):
    asset = get_object_or_404(Asset, id=pk, account__user=request.user)
    raw_quantity = request.POST.get("quantity")

    try:
        new_quantity = Decimal(raw_quantity)
        if new_quantity > 0:
            asset.quantity = new_quantity
            asset.save()
    except (InvalidOperation, TypeError):
        pass

    return redirect("account_detail", pk=asset.account.id)


@login_required
@require_POST
def delete_asset_view(request, pk):
    asset = get_object_or_404(Asset, id=pk, account__user=request.user)
    account_id = asset.account.id
    asset.delete()
    return redirect("account_detail", pk=account_id)


@login_required
@require_POST
def refresh_account_prices_view(request, pk):
    account = get_object_or_404(Account, id=pk, user=request.user)
    _update_assets_prices(account.asset_set.all())
    return redirect("account_detail", pk=account.id)