from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .models import *

# Create your views here.

def index(request):
    return render(request, 'base.html')

def products(request):
    context = {
        'items': Ticket.objects.all()
    }
    #TODO
    return render(request, "base.html", context)


class ItemDetailView(DetailView):
    model = Ticket
    template_name = "product.html"
