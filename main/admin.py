from django.contrib import admin
from .models import Ticket,Order, OrderTicket, BillingAddress

# Register your models here.



admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(OrderTicket)
admin.site.register(BillingAddress)