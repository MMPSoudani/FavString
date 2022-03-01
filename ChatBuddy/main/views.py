from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import (
    LoginForm, RegisterForm,
)
from .models import User


class HomeView(View):
    template_name = "main/home.html"
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)


class LoginView(View):
    template_name = "main/login.html"
    context = {
            "login_form": LoginForm(),
        }

    def get(self, request):
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        self.context["login_form"] = LoginForm(request.POST)
        if self.context.get("login_form").is_valid():
            form_data = self.context.get("login_form").cleaned_data
            auth_user = authenticate(email=form_data.get("email"), password=form_data.get("password"))
            if auth_user:
                login(request, auth_user)
                messages.success(request, "Successfully logged in to your account")
                return redirect("main:home")
            else:
                messages.error(request, "User authentication failed")
        
        return render(request, self.template_name, self.context)


class RegisterView(View):
    template_name = "main/register.html"
    context = {
            "register_form": RegisterForm(),
        }

    def get(self, request):
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        self.context["register_form"] = RegisterForm(request.POST)
        if self.context.get("register_form").is_valid():
            form_data = self.context.get("register_form").cleaned_data
            User.objects.create_user(email=form_data.get("email"), username=form_data.get("username"), password=form_data.get("password_1"))
            messages.success(request, "Registration finished successfully")
            return redirect("main:login")
        
        return render(request, self.template_name, self.context)



class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("main:home")