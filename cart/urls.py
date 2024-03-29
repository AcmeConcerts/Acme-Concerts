from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartSummaryView.as_view(), name='cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('payment', views.payment, name='payment'),
    path('order-summary/<pk>/', views.Summary.as_view(), name='summary'),
    path('cartupdate', views.CartUpdate, name='cartupdate'),
    path('fast-checkout/<slug>/', views.fast_checkout, name="fast-checkout"),
    path('order-summary', views.search_order,name='order-searcher')
    ]