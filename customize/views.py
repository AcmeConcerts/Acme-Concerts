from django.shortcuts import render
from customize import forms
from main.models import Order, OrderTicket, Ticket
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import DetailView, View
from django.conf import settings
from django.contrib import messages
# Create your views here.

class TicketDetailView(DetailView):
    model = Ticket
    
    template_name = "customize.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL
        context["form"] = forms.CustomizeForm()
        return context


def add_customized_to_cart(request, slug):

    if request.method == 'POST':
        form = forms.CustomizeForm(request.method)
        quantity = int(request.POST.get('quantity'))

    ticket = get_object_or_404(Ticket, slug=slug)

    order_qs, order_created = Order.objects.get_or_create(user=request.user, ordered=False)
    

    order_ticket, created = OrderTicket.objects.get_or_create( 
        #Si lo encuentra, created deberia ser false
        ticket=ticket,
        user=request.user,
        ordered=False,
        order=order_qs,
        model = request.POST.get('model'),
        color = request.POST.get('color'),
        typing = request.POST.get('typing'),
        customized=True,
        quantity = quantity
    )

     # check if the order item is in the order
    if not created:
        order_ticket.quantity += quantity
        order_ticket.save()
        messages.info(request, "Cantidad de este ticket actualizada.")
    else: #Si no estaba se abrá creado, simplemente guardamos
        ticket.stock -= quantity
        ticket.save()

        order_ticket.save()
        messages.info(request, "Añadido al carro.")




    return redirect("main:ticket", slug=slug)
    
