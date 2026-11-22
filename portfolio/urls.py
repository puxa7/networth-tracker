from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("add-account/", views.add_account_view, name="add_account"),
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="portfolio/login.html",
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("home/", views.home_view, name="home"),
    path("accounts/<int:pk>/", views.account_detail_view, name="account_detail"),
    path("refresh-prices/", views.refresh_prices_view, name="refresh_prices"),
    path("accounts/<int:pk>/edit/", views.edit_account_view, name="edit_account"),
    path("register/", views.register_view, name="register"),
    path("settings/", views.settings_view, name="settings"),
    path("settings/delete-account/", views.delete_user_view, name="delete_user"),
    path("accounts/<int:pk>/delete/", views.delete_account_view, name="delete_account"),
    path("assets/<int:pk>/edit-quantity/", views.edit_asset_quantity_view, name="edit_asset_quantity"),
    path("assets/<int:pk>/delete/", views.delete_asset_view, name="delete_asset"),
    path("accounts/<int:pk>/refresh-prices/", views.refresh_account_prices_view, name="refresh_account_prices"),
    path("asset/<int:pk>/edit/", views.edit_asset_view, name="edit_asset"),
]
