from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from AcmeConcerts.forms import CheckoutForm
from main.models import Order, OrderTicket, Ticket
from django.contrib.auth.decorators import login_required
import braintree
from django.conf import settings


def index(request):
    return render(request, 'cart.html')


class OrderSummaryView(View):
    
    def get(self, *args, **kwargs):
        try:
            
            order = Order.objects.get(user = self.request.user, ordered = False)
            tickets = OrderTicket.objects.filter(order=order)
            
            context = {
                'object' : order,
                'tickets' : tickets,
                'tickets_num' : len(tickets),
                'MEDIA_URL' : settings.MEDIA_URL
            }
            print("hola")
            return render(self.request, 'cart.html', context)
        except:
            messages.error(self.request, "No tienes ningun pedido activo")
            return redirect("cart")

def CartUpdate(request):
    ticket_slug = request.POST['ticket_slug']
    number = request.POST['number']
    order = Order.objects.get(user = request.user, ordered = False)
    ticket = Ticket.objects.get(slug= ticket_slug)
    order_ticket = OrderTicket.objects.get(order=order,ticket=ticket)
    order_ticket.quantity= number
    order_ticket.save()
    return HttpResponse("Ok")

        

class CheckoutView(View):
    
    
    def get(self, *args, **kwargs):
        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        # Configure Braintree
        braintree.Configuration.configure(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )
    
        try:
            braintree_client_token = braintree.ClientToken.generate({ "customer_id": self.user.id })
        except:
            braintree_client_token = braintree.ClientToken.generate({})

        form = CheckoutForm()
        context = {
            'braintree_client_token': braintree_client_token,
            'form': form
        }
        return render(self.request, 'checkout.html',context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            return redirect("cart")
        messages.warning(self.request, "Error en el checkout")
        return redirect("cart")

@login_required
def payment(request):
    nonce_from_the_client = request.POST['paymentMethodNonce']
    customer_kwargs = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
    }
    customer_create = braintree.Customer.create(customer_kwargs)
    customer_id = customer_create.customer.id
    result = braintree.Transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    print(result)
    return redirect("main:home")

