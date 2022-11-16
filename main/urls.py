from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('tickets', views.products, name='tickets'),
    path('tickets/<slug>/', views.TicketDetailView.as_view(), name='ticket'),
]