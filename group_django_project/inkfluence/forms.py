# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models

from .models import *


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, help_text='Required.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'role')


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'genre', 'description', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(choices=GENRES, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Story Title"
        self.fields['genre'].label = "Story Genre"
        self.fields['description'].label = "Brief Description"
        self.fields['content'].label = "Story Content"
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'genre_likes']
