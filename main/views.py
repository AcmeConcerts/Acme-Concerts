from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.conf import settings
from django.contrib.auth.decorators import login_required

from AcmeConcerts import forms
from cart.views import fast_checkout
from .models import *
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def index(request):
    return render(request, 'base.html')

def products_reggaeton(request):
    context = {
        'items': Ticket.objects.filter(category = 'Rg'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Reggaeton" 
    }
    return render(request, "categorias.html", context)

def products_pop(request):
    context = {
        'items': Ticket.objects.filter(category = 'P'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Pop" 
    }
    return render(request, "categorias.html", context)

def products_indie(request):
    context = {
        'items': Ticket.objects.filter(category = 'I'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Indie" 
    }
    return render(request, "categorias.html", context)

def products_hiphop(request):
    context = {
        'items': Ticket.objects.filter(category = 'HH'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Hip Hop" 
    }
    return render(request, "categorias.html", context)

def products_rock(request):
    context = {
        'items': Ticket.objects.filter(category = 'R'),
        "MEDIA_URL" : settings.MEDIA_URL,
        "categoria" : "Rock" 
    }
    return render(request, "categorias.html", context)

def devoluciones(request):
    return render(request, "politica_devoluciones.html")

def contacto(request):
    return render(request, "atencion_cliente.html")

def contacto(request):
    return render(request, "politica_envios.html")

def privacidad(request):
    context = {
        "MEDIA_URL" : settings.MEDIA_URL,
    }
    return render(request, "privacidad.html", context)

def terminos_servicio(request):
    context = {
        "MEDIA_URL" : settings.MEDIA_URL,
    }
    return render(request, "terminosServicio.html", context)

@login_required
def add_to_cart(request, slug):
    if "fast-checkout" in request.POST:
        return fast_checkout(request,slug)
    ticket = get_object_or_404(Ticket, slug=slug)
    quantity = 1

    if request.method == 'POST':
        form = forms.QuantityForm(request.method)
        quantity = int(request.POST.get('quantity'))

    order_qs, order_created = Order.objects.get_or_create(user=request.user, ordered=False)
    

    order_ticket, created = OrderTicket.objects.get_or_create( 
        #Si lo encuentra, created deberia ser false
        ticket=ticket,
        user=request.user,
        ordered=False,
        order=order_qs,
        customized=False,

    )

    # check if the order item is in the order
    if not created:
        order_ticket.quantity += quantity
        order_ticket.save()
        messages.info(request, "Cantidad de este ticket actualizada.")
    else: #Si no estaba se abrá creado, simplemente guardamos
        order_ticket.quantity = quantity
        order_ticket.save()
        messages.info(request, "Añadido al carro.")

    ticket.stock -= quantity
    ticket.save()

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
        ordered_tickets = OrderTicket.objects.filter(order=order)
        if ordered_tickets.filter(ticket=ticket).exists():
            ordered_ticket = OrderTicket.objects.filter(
                ticket=ticket,
                user=request.user,
                ordered=False
            )[0]
            ticket.stock+=ordered_ticket.quantity
            ticket.save()
            ordered_ticket.delete()
            messages.info(request, "El ticket ha sido borrado.")
            return redirect("cart")
        else:
            messages.info(request, "El ticket no estaba en tu carrito.")
            return redirect("main:ticket", slug=slug)
    else:
        messages.info(request, "No tienes ninguna orden activa.")
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
        context['form'] = forms.QuantityForm()
        return context

class HomeView(ListView):
    model = Ticket
    paginate_by = 10
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL

        queryset = self.request.GET.get("buscador") 

        category_reverse = dict((v, k) for k, v in CATEGORY)
        try:
            if queryset: 
                context["tickets"] = Ticket.objects.filter(
                    Q(title__icontains = queryset) |
                    Q(category__icontains = category_reverse[queryset.capitalize()]) |
                    Q(slug__icontains = queryset)
                ).distinct()
            else:
                context["tickets"] = Ticket.objects.all()
        except:
            if queryset: 
                context["tickets"] = Ticket.objects.filter(
                    Q(title__icontains = queryset) |
                    Q(slug__icontains = queryset)
                ).distinct()
            else:
                context["tickets"] = Ticket.objects.all()
        
        return context
