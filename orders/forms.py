from django import forms
from .models import Order, TextArea, PostCode


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        # widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Иван', 'aria-label': 'Иван'}),
        #            'last_name': forms.TextInput(attrs={'placeholder': 'Иванов', 'aria-label': 'Иванов'}),
        #            'address': forms.TextInput(
        #                attrs={'placeholder': 'Проспект Ленина', 'aria-label': 'Проспект Ленина'}),
        #            'city': forms.TextInput(attrs={'placeholder': 'Рязань', 'aria-label': 'Рязань'})}
    
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.CharField()
    address=forms.CharField()
    postal_code=forms.CharField()
    city=forms.CharField()

class TextAreaCraeteForm(forms.ModelForm):
    class Meta:
        model= TextArea
        fields = ['text']
    
    text = forms.CharField()

class PostCodeCreateForm(forms.ModelForm):
    class Meta:
        model = PostCode
        fields = ['order_code']

    order_code = forms.CharField()

