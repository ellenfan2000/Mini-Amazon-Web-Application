from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from crispy_forms.layout import Layout, Fieldset, Row, Column
from crispy_forms.helper import FormHelper
class RegForm(UserCreationForm):
    email=forms.EmailField(required=True)       
    class Meta:
        model = User
        fields = ["username", "email","password1", "password2"]

class EmailForm(forms.Form): 
    email=forms.EmailField(required=True,label="New Email Address",initial="XXXX@XX.XXX")  
    
class BuyForm(forms.Form):
    amount = forms.IntegerField(initial=1,validators=[MinValueValidator(1)],label="Purchase Amount")  
        
    first_name=forms.CharField(required=True, label="First Name")
    last_name=forms.CharField(required=True, label="Last Name")
    phone_number = forms.CharField(required=False,label="Phone Number")
    address_x = forms.IntegerField(required=True,label="X") 
    address_y = forms.IntegerField(required=True,label="Y") 
    
    card_number = forms.CharField(required=True,label="Card Number")    
    expires = forms.CharField(required=True,label="Expires")
    security_code = forms.CharField(required=True, label="Security Code")
  
    
