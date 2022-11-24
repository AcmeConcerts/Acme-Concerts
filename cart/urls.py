from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),

]