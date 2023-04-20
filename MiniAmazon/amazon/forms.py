from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegForm(UserCreationForm):
    email=forms.EmailField(required=True)       
    class Meta:
        model = User
        fields = ["username", "email","password1", "password2"]

class EmailForm(forms.Form): 
    email=forms.EmailField(required=True,label="New Email Address",initial="XXXX@XX.XXX")  
