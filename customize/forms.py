from django import forms

from main import models

class CustomizeForm(forms.Form):
    model = forms.ChoiceField(choices=models.OrderTicket.MODEL,label='Modelo', widget=forms.Select(attrs={
        'class': 'form-select w-100'
    }))
    color = forms.ChoiceField(choices=models.OrderTicket.COLOR,label='Color', widget=forms.Select(attrs={
        'class': 'form-select w-100'
    }))
    typing = forms.ChoiceField(choices=models.OrderTicket.TYPING, label='Tipografía', widget=forms.Select(attrs={
        'class': 'form-select w-100'
    }))
    quantity = forms.IntegerField()
    
