from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from AcmeConcerts.forms import CITY_CHOICES, COUNTRY_CHOICES, CheckoutForm
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
    number = int(request.POST['number'])
    order = Order.objects.get(user = request.user, ordered = False)
    ticket = Ticket.objects.get(slug= ticket_slug)
    order_ticket = OrderTicket.objects.get(order=order,ticket=ticket)
    difference = order_ticket.quantity - number
    ticket.stock += difference
    ticket.save()
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
    quantity = request.POST.get('quantity')
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
    order_ticket= OrderTicket.objects.create(ticket=ticket,order = order, quantity=quantity)
    
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
        if (request.user.is_authenticated):
            tickets = OrderTicket.objects.filter(order=order)
            country_dic = dict((v, k) for v, k in COUNTRY_CHOICES)
            city_dic = dict((v, k) for v,k in CITY_CHOICES) 
            message = 'Enhorabuena, has realizado una compra en Acme Concerts. Te adjuntamos la factura de compra de tu pedido con id ' + str(order.id) +  '. ¡Ahora solo queda disfrutar!\n\n'
            total_price = 0.
            
            for ticket in tickets:
                if ticket.customized:
                    price = ticket.ticket.price_customized * float(ticket.quantity)
                else:
                    price = ticket.ticket.price * float(ticket.quantity)

                total_price += price
                message += ticket.ticket.title + "             Cantidad: " + str(ticket.quantity) + "             Precio: " + str(price) + "\n"
            message+= "El importe total es de: " + str(total_price) + "0€\n|n "
            if (order.billing_address.optional_address != ""):
                message+= "Tus entradas serán enviadas a " + order.billing_address.main_address + " más especificamente a" + order.billing_address.optional_address + " en " + city_dic.get(order.billing_address.city) +" con codigo postal " + order.billing_address.cp + ", " + country_dic.get(order.billing_address.country)
            
            else:
                message+= "Tus entradas serán enviadas a " + order.billing_address.main_address + " en " + city_dic.get(order.billing_address.city) +" con codigo postal " + order.billing_address.cp + ", " + country_dic.get(order.billing_address.country)

            message += "\nPuedes conocer el estado de tu pedido a traves del enlace: http://acmeconcerts.pythonanywhere.com/cart/order-summary/" + str(order.id) + "/. Para cualquier duda puedes contactar con nosotros a través del apartado Contacto. "
            mail = EmailMessage(
                'Compra realizada',
                message,
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
        for ticket in tickets:
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

    
    

