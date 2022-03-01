from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .forms import (
    LoginForm, RegisterForm, SearchForm,
    CreateRoomForm, ProfileUpdateForm,
)
from .models import User, Topic, Room


class HomeView(View):
    template_name = "main/home.html"

    def get(self, request):
        context = {
        "search_form": SearchForm(request.GET or None)
        }
        return render(request, self.template_name, context)


class LoginView(View):
    template_name = "main/login.html"
    
    def get(self, request):
        context = {
            "login_form": LoginForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = {
            "login_form": LoginForm(request.POST),
        }
        if self.context.get("login_form").is_valid():
            form_data = self.context.get("login_form").cleaned_data
            auth_user = authenticate(email=form_data.get("email"), password=form_data.get("password"))
            if auth_user:
                login(request, auth_user)
                messages.success(request, "Successfully logged in to your account")
                return redirect("main:home")
            else:
                messages.error(request, "User authentication failed")
        
        return render(request, self.template_name, context)


class RegisterView(View):
    template_name = "main/register.html"

    def get(self, request):
        context = {
            "register_form": RegisterForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = {
            "register_form": RegisterForm(request.POST),
        }
        if self.context.get("register_form").is_valid():
            form_data = self.context.get("register_form").cleaned_data
            User.objects.create_user(email=form_data.get("email"), username=form_data.get("username"), password=form_data.get("password_1"))
            messages.success(request, "Registration finished successfully")
            return redirect("main:login")
        
        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("main:home")


class ProfileOverView(View):
    template_name = "main/profile.html"

    def get(self, request, username):
        context = {
            "user": get_object_or_404(User, username=username),
            "path": request.META.get("PATH_INFO").split("/")[-2],
        }
        return render(request, self.template_name, context)


class ProfilUpdateView(View):
    temaplte_name = "main/profile.html"

    def get(self, request, username):
        context = {
            "user": get_object_or_404(User, username=username),
            "path": request.META.get("PATH_INFO").split("/")[-2],
        }
        context["profile_update_form"] = ProfileUpdateForm(instance=context.get("user").profile)
        return render(request, self.temaplte_name, context)
    
    def post(self, request, username):
        context = {
            "user": get_object_or_404(User, username=username),
            "path": request.META.get("PATH_INFO").split("/")[-2],
        }
        context["profile_update_form"] = ProfileUpdateForm(request.POST, request.FILES, instance=context.get("user").profile)
        if context.get("profile_update_form").is_valid():
            context.get("profile_update_form").save()
            messages.success(request, "Profile updated successfully")
            return redirect("main:profile_overview", username)

        return render(request, self.temaplte_name, context)


class CreateRoomView(View):
    template_name = "main/create_room.html"

    def get(self, request):
        context = {
            "create_room_form": CreateRoomForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = {
            "create_room_form": CreateRoomForm(request.POST),
        }
        if context.get("create_room_form").is_valid():
            form_data = context.get("create_room_form").cleaned_data
            topic = Topic.objects.get(name=form_data.get("topic"))
            Room.objects.create(topic=topic, host=request.user, title=form_data.get("title"), description=form_data.get("description"))
            messages.success(request, f"The Room \"{form_data.get('title')}\" was created successfully")
            return redirect("main:home")
        
        return render(request, self.template_name, context)