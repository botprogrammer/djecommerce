from django import forms

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder':'1234 Main St',
        'class':'form-control',
        'id':'address'
    }))
    zip = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder':'123456',
        'class':'form-control',
        'id':'zip'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder':'you@example.com',
        'class':'form-control',
        'id':'email'
    }))
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
