from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    RuleListView,
    RuleDetailView,
    ProductListView,
    ProductDetailView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/me/", MeView.as_view()),
    path("rules/", RuleListView.as_view()),
    path("rules/<int:pk>/", RuleDetailView.as_view()),
    path("products/", ProductListView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
]
