from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm, AssetForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Asset, UserProfile
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


def _get_exchange_rate(from_currency, to_currency, cache):
    if from_currency == to_currency:
        return Decimal("1")

    pair = f"{from_currency}{to_currency}=X"
    if pair not in cache:
        try:
            rate = yf.Ticker(pair).fast_info["last_price"]
            cache[pair] = Decimal(str(rate)) if rate else Decimal("1")
        except Exception:
            cache[pair] = Decimal("1")

    return cache[pair]    
    

@login_required
def home_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    target_currency = profile.display_currency
    accounts = Account.objects.filter(
        user=request.user).prefetch_related("asset_set")

    rates_cache = {}
    net_worth = Decimal("0.00")
    
    for account in accounts:
        for asset in account.asset_set.all():
            rate = _get_exchange_rate(asset.currency, target_currency, rates_cache)
            net_worth += asset.total_value * rate

    return render(request, "portfolio/home.html", {
        "accounts": accounts,
        "net_worth": net_worth,
        "display_currency": target_currency,
    })


@login_required
def account_detail_view(request, pk):
    account = get_object_or_404(Account, id=pk, user=request.user)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    target_currency = profile.display_currency

    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.account = account

            if asset.price is None:
                asset.price = Decimal("0.00")
                asset.save()
                _update_assets_prices([asset])
            else:
                asset.save()

            return redirect("account_detail", pk=account.id)
    else:
        form = AssetForm()

    assets = list(account.asset_set.all())
    rates_cache = {}
    account_total_value = Decimal("0.00")

    for asset in assets:
        rate = _get_exchange_rate(asset.currency, target_currency, rates_cache)
        asset.converted_total_value = asset.total_value * rate
        account_total_value += asset.converted_total_value

    return render(request, "portfolio/account_detail.html", {
        "account": account,
        "assets": assets,
        "form": form,
        "account_total_value": account_total_value,
        "display_currency": target_currency,
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
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        currency = request.POST.get("display_currency")
        valid_currencies = dict(UserProfile.CURRENCY_CHOICES)
        if currency in valid_currencies:
            profile.display_currency = currency
            profile.save()
        return redirect("settings")

    return render(request, "portfolio/settings.html", {
        "profile": profile,
        "currencies": UserProfile.CURRENCY_CHOICES,
    })


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
