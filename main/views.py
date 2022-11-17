from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.conf import settings
from django.contrib.auth.decorators import login_required
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

@login_required
def add_to_cart(request, slug):
    #TODO
    pass


@login_required
def remove_from_cart(request, slug):
    #TODO
    pass


@login_required
def remove_single_item_from_cart(request, slug):
    #TODO
    pass

class TicketDetailView(DetailView):
    model = Ticket
    
    template_name = "product.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL
        context["tickets"] = Ticket.objects.all()[:3]
        return context
