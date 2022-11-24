from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages


from AcmeConcerts.forms import CheckoutForm

def index(request):
    return render(request, 'cart.html')

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'cart.html')

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