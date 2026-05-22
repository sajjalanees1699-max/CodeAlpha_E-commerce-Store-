from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone', 'address', 'city', 'postal_code', 'payment_method')
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-input'}),
            'address': forms.Textarea(attrs={'placeholder': 'Street Address', 'class': 'form-input', 'rows': 3}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-input'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code', 'class': 'form-input'}),
            'payment_method': forms.Select(
                choices=[
                    ('Cash on Delivery', 'Cash on Delivery'),
                    ('Credit Card', 'Credit Card'),
                    ('Bank Transfer', 'Bank Transfer'),
                ],
                attrs={'class': 'form-input'}
            ),
        }
