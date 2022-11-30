from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.OrderSummaryView.as_view(), name='cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('payment', views.payment, name='payment'),
    path('cartupdate', views.CartUpdate, name='cartupdate'),
    path('fast-checkout/<slug>/', views.fast_checkout, name="fast-checkout"),
]