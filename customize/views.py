from django.shortcuts import render
from main.models import Ticket
from django.views.generic import DetailView
from django.conf import settings
# Create your views here.

def index(request):
    return render(request, 'base.html')

class TicketDetailView(DetailView):
    model = Ticket
    
    template_name = "customize.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context