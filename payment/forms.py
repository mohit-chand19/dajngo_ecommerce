from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    full_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Full Name'}), required=True)
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}), required=True)
    address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address1'}), required=True)
    address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address2'}), required=False)
    city = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter City'}), required=True)
    province = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Province'}), required=True)
    zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Zipcode(if any)'}), required=False)
    country = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Country Name'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['full_name','email','address1','address2','city','province','zipcode','country']
        exclude = ['user',]


class PaymentForm(forms.Form):
    card_name= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Card Holder Name'}), required=True)
    card_number= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Card Number'}), required=True)
    card_expiry_date= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Card Expiration Date'}), required=True)
    card_cvv_number= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter CVV Code'}), required=True)
    card_address1= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Billing Address1'}), required=True)
    card_address2= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Billing Address2'}), required=False)
    card_city= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Billing City'}), required=True)
    card_province= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Billing Province'}), required=True)
    card_zipcode= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Billing Zipcode'}), required=False)
    card_country= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Billing Country'}), required=True)
