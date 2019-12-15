from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'password1', 'password2', 'language') 

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Минимум 8 символов. Не может состоять только из цифр.'
        self.fields['language'].label = 'Язык/language'


class CustomAuthenticationForm(AuthenticationForm):
        model = User