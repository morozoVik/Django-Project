from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'})
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'country', 'avatar')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите страну'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )