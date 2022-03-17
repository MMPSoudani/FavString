from re import compile
from django import forms
from main.models import User, AuthUser
from django.db.models import Q


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is not registered")
        return username


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    is_super = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "is_super", "password"]
    

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username
    

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        pattern = compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$+-_])[a-zA-Z0-9!@#$+-_]{8,30}$")
        if not pattern.fullmatch(password):
            raise forms.ValidationError("Must be 8-30 chars and include at least one of en letters, EN letters, digits and !@#$+-_")
        return password
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password


class LogoutForm(forms.Form):
    auth_users = AuthUser.objects.all()
    choices = [(user.user.username, user.user.username) for user in auth_users]
    
    username = forms.ChoiceField(choices=tuple(choices))


class AddStringForm(forms.Form):
    super_users = AuthUser.objects.filter(Q(user__is_super=True))
    choices = [(user.user.username, user.user.username) for user in super_users]

    username = forms.ChoiceField(choices=tuple(choices))
    string = forms.CharField(widget=forms.Textarea)


class LikeStringForm(forms.Form):
    users = AuthUser.objects.all()
    choices = [(user.user.username, user.user.username) for user in users]

    username = forms.ChoiceField(label="", choices=tuple(choices))