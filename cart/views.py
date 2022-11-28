from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from AcmeConcerts.forms import CheckoutForm
from main.models import BillingAddress, Order, OrderTicket, Ticket
from django.contrib.auth.decorators import login_required
import braintree
from django.conf import settings


def index(request):
    return render(request, 'cart.html')


class OrderSummaryView(View):
    
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
            messages.error(self.request, "Es necesario iniciar sesión para acceder a Mi Carrito")
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

        order = Order.objects.get(user = self.request.user, ordered = False)
        tickets = OrderTicket.objects.filter(order=order)

        context = {
            'braintree_client_token': braintree_client_token,
            'form': form,
            'tickets': tickets,
            'tickets_num' : len(tickets)
        }
        return render(self.request, 'checkout.html',context)
    '''
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            if form.is_valid():
                firstname = form.cleaned_data.get('firstname')
                lastname = form.cleaned_data.get('lastname')
                main_address = form.cleaned_data.get('main_address')
                optional_address = form.cleaned_data.get('optional_address')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                cp = form.cleaned_data.get('cp')
                payment_option = form.cleaned_data.get('payment_option')
                billingAddress = BillingAddress(
                    user = self.request.user,
                    firstname = firstname,
                    lastname = lastname,
                    main_address = main_address, 
                    optional_address = optional_address, 
                    country = country,
                    city = city, 
                    cp = cp
                )

                billingAddress.save()
                order.billing_address = billingAddress
                order.save()

                messages.warning(self.request, "El formulario es válido")
                return redirect("cart")
            
            messages.warning(self.request, "El formulario no es válido")
            return redirect("cart")
        except:
            messages.error(self.request, "No tienes ningun pedido activo")
            return redirect("cart")
    '''
        
@login_required
def payment(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    main_address = request.POST['main_address']
    optional_address = request.POST['optional_address']
    country = request.POST['country']
    city = request.POST['city']
    cp = request.POST['cp']
    payment_option = request.POST['payment_option']
    try:
        order = Order.objects.get(user = request.user, ordered = False)
        billingAddress = BillingAddress(
            user = request.user,
            firstname = firstname,
            lastname = lastname,
            main_address = main_address, 
            optional_address = optional_address, 
            country = country,
            city = city, 
            cp = cp
        )
        billingAddress.save()
        order.billing_address = billingAddress
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
        return redirect("cart")
        
    except:
        messages.error(request, "No tienes ningun pedido activo")
        return redirect("cart")
    
    

