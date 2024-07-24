from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from cupclub.predictions.views import CapperListView, SubscriberListView

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "cappers/",
        CapperListView.as_view(),
        name="capper-list",
    ),
    path(
        "subscribers/",
        SubscriberListView.as_view(),
        name="subscriber-list",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
]
