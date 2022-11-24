from django import forms

PAYMENT_CHOICES = (
    ('T','Pago con tarjeta'),
    ('P','Paypal')
)

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

class CheckoutForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    lastname = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    main_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    optional_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    country = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'custom-select d-block w-100'}), choices = COUNTRY_CHOICES)

    city = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'custom-select d-block w-100'}), choices = CITY_CHOICES)
    
    cp = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices= PAYMENT_CHOICES)
 