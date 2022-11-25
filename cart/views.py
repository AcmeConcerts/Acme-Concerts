from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from AcmeConcerts.forms import CheckoutForm
from main.models import Order

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