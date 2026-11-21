from django.urls import path
from .views import add_account_view, home_view, account_detail_view, refresh_prices_view, edit_account_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("add-account/", add_account_view, name="add_account"),
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="portfolio/login.html",
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("home/", home_view, name="home"),
    path("accounts/<int:pk>/", account_detail_view, name="account_detail"),
    path("refresh-prices/", refresh_prices_view, name="refresh_prices"),
    path("accounts/<int:pk>/edit/", edit_account_view, name="edit_account"),
]
