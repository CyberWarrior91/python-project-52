from django import forms
from django.contrib.auth.models import User

from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, MultiField, Div, Field
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    """
    Class to handle a form to register a user with
    certain fields that are required
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "username",
                  "password1", "password2")

    def save(self, commit=True):
        """
        Saves the form in db if valid
        :return: new user information
        """
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user
        
