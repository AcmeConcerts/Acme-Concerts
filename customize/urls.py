from django.urls import path

from . import views

urlpatterns = [
    path('<slug>/', views.TicketDetailView.as_view(), name='customize'),
]