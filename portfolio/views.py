from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm, AssetForm
from django.contrib.auth.decorators import login_required
from .models import Account



@login_required
def home_view(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, "portfolio/home.html", {"accounts": accounts})


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
