from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderSummaryView.as_view(), name='cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('payment', views.payment, name='payment'),
    path('cartupdate', views.CartUpdate, name='cartupdate')
]