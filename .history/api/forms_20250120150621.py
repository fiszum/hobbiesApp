from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Hobby
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        s
        required=False
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # HTML5 date picker
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth', 'hobbies']


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password.")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
        return cleaned_data
    