from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartSummaryView.as_view(), name='cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('payment', views.payment, name='payment'),
    path('order-summary', views.summary, name='summary'),
    path('cartupdate', views.CartUpdate, name='cartupdate')
]