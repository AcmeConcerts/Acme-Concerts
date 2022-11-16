from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def products(request):
    context = {
        'items': Ticket.objects.all()
    }
    return render(request, "products.html", context)