from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Q

from main.models import User, AuthUser, String
from main.forms import LoginForm, RegisterForm, LogoutForm, AddStringForm, LikeStringForm


class HomeView(View):
    template_name = "main/index.html"

    def get(self, request):
        context = {
            "strings": String.objects.all(),
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
        if context.get("login_form").is_valid():
            form_data = context.get("login_form").cleaned_data
            user = get_object_or_404(User, username=form_data.get("username"))
            if form_data.get("password") == user.password:
                user.last_login = datetime.now()
                user.save()
                AuthUser.objects.create(user=user, is_authenticated=True)
                messages.success(request, f"{user.username} logged in successfully")
                return redirect("main:home")
            else:
                messages.error(request, "User Authentication Failed")
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
        if context.get("register_form").is_valid():
            username = context.get("register_form").cleaned_data.get("username")
            context.get("register_form").save()
            messages.success(request, f"{username} registered successfully")
            return redirect("main:login")
        return render(request, self.template_name, context)


class LogoutView(View):
    template_name = "main/logout.html"

    def get(self, request):
        context = {
            "logout_form": LogoutForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = {
            "logout_form": LogoutForm(request.POST),
        }
        if context.get("logout_form").is_valid():
            username = context.get("logout_form").cleaned_data.get("username")
            user = get_object_or_404(AuthUser, Q(user__username__contains=username))
            user.delete()
            messages.success(request, f"{username} is now logged out")
            return redirect("main:home")
        return render(request, self.template_name, context)


class AddStringView(View):
    template_name = "main/add_string.html"

    def get(self, request):
        context = {
            "add_string_form": AddStringForm(),
            "super_users": AuthUser.objects.filter(Q(user__is_super=True)).count(),
        }
        if context.get("super_users") == 0:
            messages.info(request, "No super user exists, only super users can add strings")
            return redirect("main:home")
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = {
            "add_string_form": AddStringForm(request.POST),
        }
        if context.get("add_string_form").is_valid():
            form_data = context.get("add_string_form").cleaned_data
            user = get_object_or_404(User, username=form_data.get("username"))
            String.objects.create(user=user, string=form_data.get("string"))
            messages.success(request, "The new string was added successfullt")
            return redirect("main:home")
        return render(request, self.template_name, context)


class StringOverView(View):
    template_name = "main/string_overview.html"

    def get(self, request, id):
        context = {
            "string": get_object_or_404(String, id=id),
            "like_string_form": LikeStringForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        context = {
            "string": get_object_or_404(String, id=id),
            "like_string_form": LikeStringForm(request.POST),
        }
        if context.get("like_string_form").is_valid():
            username = context.get("like_string_form").cleaned_data.get("username")
            user = get_object_or_404(User, username=username)
            if context.get("string").favored_by.filter(username=user.username):
                messages.error(request, f"{user.username} have already liked this post")
                return redirect("main:string_overview", id)
            else:
                context.get("string").favored_by.add(user)
                messages.success(request, f"{username} liked \"{context.get('string').string[:20]}...\"")
                return redirect("main:string_overview", id)
        return render(request, self.template_name, context)