from django.http import HttpResponse
from django.shortcuts import render

from .models import *

# Create your views here.

def index(request):
    return render(request, 'base.html')

def products(request):
    context = {
        'items': Ticket.objects.all()
    }
    return render(request, "products.html", context)