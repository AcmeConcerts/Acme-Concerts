from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tickets', views.products, name='tickets'),
    path('tickets/<slug>/', views.TicketDetailView.as_view(), name='ticket'),
]