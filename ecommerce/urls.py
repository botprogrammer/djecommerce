from django.urls import path
from .views import (
    HomeView,
    CartView,
    add_to_cart,
    remove_from_cart,
    remove_one_from_cart,
    CheckoutView,
    ProductDetailView,
    PaymentView
)
app_name = 'ecommerce'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),    
    path('cart/', CartView.as_view(), name='cart'),    
    path('add-to-cart/<slug>/<str:pk>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/<str:pk>/', remove_from_cart, name='remove_from_cart'),
    path('remove-single-item/<slug>/<str:pk>/', remove_one_from_cart, name='remove_one_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/<slug>/<str:pk>/', ProductDetailView.as_view(), name='product'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
]

