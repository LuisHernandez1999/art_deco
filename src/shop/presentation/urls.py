from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("sobre/", views.about, name="about"),
    path("informacoes/", views.information, name="information"),
    path("catalogo/", views.catalog, name="catalog"),
    path("pecas/<slug:slug>/", views.product_detail, name="product_detail"),
    path("carrinho/", views.cart, name="cart"),
    path("carrinho/adicionar/<slug:slug>/", views.cart_add, name="cart_add"),
    path("carrinho/atualizar/<int:product_id>/", views.cart_update, name="cart_update"),
    path("finalizar/", views.checkout, name="checkout"),
    path("pedidos/<uuid:reference>/", views.order_confirmation, name="order_confirmation"),
]