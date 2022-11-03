from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

Creator = get_user_model()


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'publish']


class CreatorCreationForm(UserCreationForm):
    class Meta:
        model = Creator
        fields = ['username', 'email', 'password1', 'password2']


class CreatorUpdateForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['email', 'bio', 'avatar']
