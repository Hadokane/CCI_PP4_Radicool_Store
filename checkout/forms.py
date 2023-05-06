from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email',
                  'street_address_1', 'street_address_2',
                  'town_or_city', 'postcode',
                  'county', 'country',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders rather than using labels.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'street_address_1': 'Street Address 1',
            'street_address_2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'postcode': 'Postal Code',
            'county': 'County/State',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'  # *=required
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
