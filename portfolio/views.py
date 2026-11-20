from django.shortcuts import render, redirect
from .forms import AccountForm
from django.contrib.auth.decorators import login_required



@login_required
def home_view(request):
    return render(request, "portfolio/home.html")


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
