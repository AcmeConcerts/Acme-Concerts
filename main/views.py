from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'base.html')

def products(request):
    context = {
        'items': Ticket.objects.all()
    }
    #TODO
    return render(request, "base.html", context)

def products_reggaeton(request):
    print(Ticket.objects.values())
    context = {
        'items': Ticket.objects.filter(category = 'Rg'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Reggaeton" 
    }
    return render(request, "categorias.html", context)

def products_pop(request):
    print(Ticket.objects.values())
    context = {
        'items': Ticket.objects.filter(category = 'P'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Pop" 
    }
    return render(request, "categorias.html", context)

def products_indie(request):
    print(Ticket.objects.values())
    context = {
        'items': Ticket.objects.filter(category = 'I'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Indie" 
    }
    return render(request, "categorias.html", context)

def products_hiphop(request):
    print(Ticket.objects.values())
    context = {
        'items': Ticket.objects.filter(category = 'HH'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Hip Hop" 
    }
    return render(request, "categorias.html", context)

def products_rock(request):
    print(Ticket.objects.values())
    context = {
        'items': Ticket.objects.filter(category = 'r'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Rock" 
    }
    return render(request, "categorias.html", context)

@login_required
def add_to_cart(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    order_ticket, created = OrderTicket.objects.get_or_create(
        ticket=ticket,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.tickets.filter(ticket__slug=ticket.slug).exists():
            order_ticket.quantity += 1
            order_ticket.save()
            messages.info(request, "This item quantity was updated.")
        else:
            order.tickets.add(order_ticket)
            messages.info(request, "This item was added to your cart.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.tickets.add(order_ticket)
        messages.info(request, "This item was added to your cart.")
    return redirect("main:ticket", slug=slug)


@login_required
def remove_from_cart(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.tickets.filter(ticket__slug=ticket.slug).exists():
            order_ticket = OrderTicket.objects.filter(
                ticket=ticket,
                user=request.user,
                ordered=False
            )[0]
            order.tickets.remove(order_ticket)
            order_ticket.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("main:ticket", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("main:ticket", slug=slug)


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

class HomeView(ListView):
    model = Ticket
    paginate_by = 10
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context