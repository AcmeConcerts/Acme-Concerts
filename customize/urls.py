from django.urls import path

from . import views

app_name = "customize"

urlpatterns = [
    path('<slug>/', views.TicketDetailView.as_view(), name='customize'),
    path('<slug>/add-customized-to-cart/', views.add_customized_to_cart, name='add-customized-to-cart')
]