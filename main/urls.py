from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tickets/<slug>/', views.TicketDetailView.as_view(), name='ticket'),
    path('reggaeton', views.products_reggaeton, name='reggaeton'),
    path('pop', views.products_pop, name='pop'),
    path('indie', views.products_indie, name='indie'),
    path('hiphop', views.products_hiphop, name='hiphop'),
    path('rock', views.products_rock, name='rock'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),


]