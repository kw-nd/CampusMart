from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Listing
from .models import Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email', 'password1', 'password2']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'condition', 'photo']
        
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'condition', 'photo', 'status']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        
class BuyListingsForm(forms.Form):
    number_of_listings = forms.IntegerField(min_value=1, label="How many listings would you like to buy?")

