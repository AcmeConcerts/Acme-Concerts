from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from AcmeConcerts.forms import CheckoutForm
from main.models import BillingAddress, Order, OrderTicket, Ticket
from django.contrib.auth.decorators import login_required
import braintree
from django.conf import settings
from django.core.mail import EmailMessage

def index(request):
    return render(request, 'cart.html')


class CartSummaryView(View):
    
    def get(self, *args, **kwargs):
        try:
            order,created = Order.objects.get_or_create(user = self.request.user, ordered = False)
            tickets = OrderTicket.objects.filter(order=order)
            
            context = {
                'object' : order,
                'tickets' : tickets,
                'tickets_num' : len(tickets),
                'MEDIA_URL' : settings.MEDIA_URL
            }
            return render(self.request, 'cart.html', context)
        except:
            return redirect("/accounts/login")

def CartUpdate(request):
    ticket_slug = request.POST['ticket_slug']
    number = request.POST['number']
    order = Order.objects.get(user = request.user, ordered = False)
    ticket = Ticket.objects.get(slug= ticket_slug)
    order_ticket = OrderTicket.objects.get(order=order,ticket=ticket)
    order_ticket.quantity= number
    order_ticket.save()
    return HttpResponse("Ok")


def search_order(request):


    return render(request, 'order_search.html')

class CheckoutView(View):
    
    def get(self, *args, **kwargs):
        try:
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
            order = Order.objects.get(user = self.request.user, ordered = False)
            tickets = OrderTicket.objects.filter(order=order)
            
            billing_addresses = BillingAddress.objects.filter(user=self.request.user)
            orderId =  order.id
            context = {
                'braintree_client_token': braintree_client_token,
                'form': form,
                'order_id':orderId,
                'tickets': tickets,
                'billing_addresses' : billing_addresses,
                'tickets_num' : len(tickets)
            }
            return render(self.request, 'checkout.html',context)
        except:
            return redirect("/accounts/login")


def fast_checkout(request,slug):
    
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
        braintree_client_token = braintree.ClientToken.generate({ "customer_id": request.user.id })
    except:
        braintree_client_token = braintree.ClientToken.generate({})

    form = CheckoutForm()

    ticket = Ticket.objects.get(slug=slug)
    order = Order.objects.create(ordered=False)
    order_ticket= OrderTicket.objects.create(ticket=ticket,order = order)
    
    billing_addresses = []
    if(request.user.is_authenticated):
        billing_addresses = BillingAddress.objects.filter(user=request.user)
    
    
    context = {
                'braintree_client_token': braintree_client_token,
                'form': form,
                'billing_addresses' : billing_addresses,
                'ticket': order_ticket,
                'authenticated': request.user.is_authenticated,
                'order_id': order.id
            }
    return render(request, "fast_checkout.html", context)
    
    
        
def payment(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    main_address = request.POST['main_address']
    optional_address = request.POST['optional_address']
    country = request.POST['country']
    city = request.POST['city']
    cp = request.POST['cp']
    payment_option = request.POST['payment_option']
    save_info = request.POST['save_info']
    order_id = request.POST['order_id']
    
    try:
        order = Order.objects.get(id= order_id)
        if save_info == 'true':
            billingAddress, created = BillingAddress.objects.get_or_create(
                user = request.user,
                firstname = firstname,
                lastname = lastname,
                main_address = main_address, 
                optional_address = optional_address, 
                country = country,
                city = city, 
                cp = cp
            )
            order.billing_address = billingAddress

        order.ordered = True
        order.ordered_date = timezone.now()
        order.save()
        if payment_option == True:
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
        if (request.user.is_authenticated):
            mail = EmailMessage(
                'Compra realizada',
                'Enhorabuena, has realizado una compra en Acme Concerts. Te adjuntamos la factura de compra de tu pedido. ¡Ahora solo queda disfrutar!',
                to=[request.user.email]
            )
            mail.send()
        
        return redirect("cart")
        
    except:
        messages.error(request, "No tienes ningun pedido activo")
        return redirect("cart")


class Summary(DetailView):
    model = Order
    template_name = "order-summary.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        context["MEDIA_URL"] = settings.MEDIA_URL
        order = Order.objects.get(id=id)
        tickets = OrderTicket.objects.filter(order=order)
        print(tickets)
        for ticket in tickets:
            ticket.ticket.stock -= ticket.quantity
            print(ticket.ticket.stock)
            ticket.ticket.save()

        context = {
                'order' : order,
                'tickets' : tickets
            }
        return context

    def get(self, request, *args, **kwargs):
        from django.http import Http404
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except Http404:
            # redirect is here
            messages.error(request, "No hay ninguna orden con esa ID.")
            return redirect('/cart/order-summary')

    
    

