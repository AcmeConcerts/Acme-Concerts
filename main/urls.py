from django.urls import path

from . import views
from .views import(add_to_cart,remove_from_cart)

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tickets', views.products, name='tickets'),
    path('tickets/<slug>/', views.TicketDetailView.as_view(), name='ticket'),
    path('reggaeton', views.products_reggaeton, name='reggaeton'),
    path('pop', views.products_pop, name='pop'),
    path('indie', views.products_indie, name='indie'),
    path('hiphop', views.products_hiphop, name='hiphop'),
    path('rock', views.products_rock, name='rock'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('profile', views.profile, name='profile'),
    path('view', views.my_view, name='view')


]