from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from AcmeConcerts.forms import CheckoutForm
from main.models import Order
from django.contrib.auth.decorators import login_required
import braintree
from django.conf import settings


def index(request):
    return render(request, 'cart.html')

@login_required
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            context = {
                'object' : order
            }
            return render(self.request, 'cart.html', context)
        except:
            messages.error(self.request, "No tienes ningun pedido activo")
            return redirect("/")
        

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
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
def checkoutPay(request):
    #generate all other required data that you may need on the 
    #checkout page and add them to context.
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

    context = {'braintree_client_token': braintree_client_token}

    return render(request, 'pay.html', context)

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
    print("hola")
    return HttpResponse('Ok')

