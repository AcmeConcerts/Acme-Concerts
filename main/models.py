from django.db import models
from django.conf import settings
from django.shortcuts import reverse
# Create your models here.

CATEGORY = (
    ('Rg', 'Reggaeton'),
    ('P', 'Pop'),
    ('I', 'Indie'),
    ('HH', 'Hip hop'),
    ('R', 'Rock')
)

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    price_customized = models.FloatField()
    category = models.CharField(choices=CATEGORY, max_length=2)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to= 'images/tickets/')
    date = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:ticket", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={
            'slug': self.slug
        })

class OrderTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.ticket.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(OrderTicket)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)      

    def __str__(self):
        return self.user.username
    
class BillingAddress(models.Model):
    COUNTRY_CHOICES = (
    ('E','España'),
    )
    CITY_CHOICES = (
        ('S','Sevilla'),
        ('A','Almería'),
        ('H','Huelva'),
        ('G','Granada'),
        ('C','Cádiz'),
        ('CO','Córdoba'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    main_address = models.CharField(max_length=100)
    optional_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100,choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=100,choices=CITY_CHOICES)
    cp = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username