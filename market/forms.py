from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Listing

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email', 'password1', 'password2']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'condition', 'photo']