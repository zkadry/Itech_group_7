# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import *


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, help_text='Required.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'role')
