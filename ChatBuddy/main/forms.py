from django import forms
from .models import User
from re import compile


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered")
        return email


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    username = forms.CharField(widget=forms.TextInput())
    password_1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password_2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is registered")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is registerd")
        return username
    
    def clean_password_1(self):
        password_1 = self.cleaned_data.get("password_1")
        pattern = compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$+-_])[a-zA-Z0-9!@#$+-_]{8,24}$")
        if not pattern.fullmatch(password_1):
            raise forms.ValidationError("Must be 8-24 chars. Must include at least one of a..z, A..Z, 0-9 and !@#$+-_")
        return password_1
    
    def clean_password_2(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 != password_2:
            raise forms.ValidationError("Passwords do not match")
        return password_2