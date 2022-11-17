from django.db import models
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