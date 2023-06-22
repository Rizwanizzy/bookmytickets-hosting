from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UserProfileForm(forms.ModelForm):
    # Fields from UserProfile model
    profile_image = forms.ImageField()
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget)
    address = forms.CharField(max_length=50)
    location = forms.CharField(max_length=30)

    # Fields from User model
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    username = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=50)

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "profile_image",
            "phone",
            "address",
            "location",
        ]


class AdminProfileForm(forms.ModelForm):
    # Fields from User model
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    username = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
