from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="index"),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
]