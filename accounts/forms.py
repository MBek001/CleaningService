from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput, TextInput, Form
from django import forms

from accounts.models import ContactMessage


class LoginForm(Form):
    username = CharField(label='Username', widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'placeholder': 'Username'
    }))
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'placeholder': 'Enter your password'
    }))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control p-4', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control p-4', 'placeholder': 'Message', 'rows': 6}),
        }