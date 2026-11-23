from django.contrib import admin
from django.urls import path, include
import os


urlpatterns = [
    path("", include("portfolio.urls")),
    path(os.environ['ADMIN_URL'], admin.site.urls),
]
