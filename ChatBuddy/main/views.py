from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q

from .forms import (
    LoginForm, RegisterForm, SearchForm, CreateRoomForm,
    ProfileUpdateForm, SendMessageForm, EditRoomForm,
    EditMessageForm,
)
from .models import User, Topic, Room, Message


class HomeView(View):
    template_name = "main/home.html"

    def get(self, request):
        context = {
            "search_form": SearchForm(request.GET or None),
            "topics": Topic.objects.all(),
            "rooms": Room.objects.all(),
            "all_messages": Message.objects.all()[:10],
        }
        if context.get("search_form").is_valid():
            query = context.get("search_form").cleaned_data.get("query")
            context["rooms"] = Room.objects.filter(Q(title__icontains=query) |
                Q(description__icontains=query) | Q(topic__name__icontains=query) |
                Q(host__username__icontains=query))
        return render(request, self.template_name, context)


class LoginView(View):
    template_name = "main/login.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main:home")
        
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
        if request.user.is_authenticated:
            return redirect("main:home")

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
        if not request.user.is_authenticated:
            return redirect("main:home")
        
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


class ProfileActivityView(View):
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
        if request.user.username != username:
            messages.error(request, "You are not authorized to perform this action")
            return redirect("main:home")

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


class ProfileSettingView(View):
    template_name = "main/profile.html"

    def get(self, request, username):
        context = {
            "user": get_object_or_404(User, username=username),
            "path": request.META.get("PATH_INFO").split("/")[-2],
        }
        if request.user.username != username:
            messages.error(request, "You are not authorized to perform this action")
            return redirect("main:home")
        
        return render(request, self.template_name, context)


class PasswordChangeView(View):
    template_name = "main/profile.html"

    def get(self, request, username):
        context = {
            "user": get_object_or_404(User, username=username),
            "path": request.META.get("PATH_INFO").split("/")[-3],
            "sub_path": request.META.get("PATH_INFO").split("/")[-2],
        }
        if request.user.username != username:
            messages.error(request, "You are not authorized to perform this action")
            return redirect("main:home")
        
        context["password_change_form"] = PasswordChangeForm(user=context.get("user"))
        return render(request, self.template_name, context)
    
    def post(self, request, username):
        context = {
            "user": get_object_or_404(User, username=username),
            "path": request.META.get("PATH_INFO").split("/")[-3],
            "sub_path": request.META.get("PATH_INFO").split("/")[-2],
        }
        
        context["password_change_form"] = PasswordChangeForm(request.POST, user=context.get("user"))
        if context.get("password_change_form").is_valid():
            user = context.get("password_change_form").save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully")
            return redirect("main:profile_overview", username)

        return render(request, self.template_name, context)


class DeleteAccountView(View):
    template_name = "main/profile.html"

    def get(self, request, username):
        context = {
            "user": get_object_or_404(User, username=username),
            "path": request.META.get("PATH_INFO").split("/")[-3],
            "sub_path": request.META.get("PATH_INFO").split("/")[-2],
        }
        if request.user.username != username:
            messages.error(request, "You are not authorized to perform this action")
            return redirect("main:home")
        
        if request.user.is_superuser:
            messages.error(request, "Admins cannot delete their account from here")
            return redirect("main:profile_overview", username)
        
        return render(request, self.template_name, context)
    
    def post(self, request, username):
        context = {
            "user": get_object_or_404(User, username=username),
        }
        context.get("user").delete()
        logout(request)
        messages.success(request, "Account was deleted successfully")
        return redirect("main:home")


class CreateRoomView(View):
    template_name = "main/create_room.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("main:home")
        
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


class RoomView(View):
    template_name = "main/room.html"

    def get(self, request, title):
        context = {
            "room": get_object_or_404(Room, title=title),
            "sender": request.user,
            "path": request.META.get("PATH_INFO").split("/")[-2],
        }
        context["send_message_form"] = SendMessageForm(initial=context)
        return render(request, self.template_name, context)
    
    def post(self, request, title):
        context = {
            "room": get_object_or_404(Room, title=title),
            "sender": request.user,
        }
        context["send_message_form"] = SendMessageForm(request.POST, initial=context)
        if context.get("send_message_form").is_valid():
            context.get("send_message_form").save()
            context.get("room").participants.add(context.get("sender"))
            return redirect("main:room", title)
        
        return render(request, self.template_name, context)


class UpdateRoomView(View):
    template_name = "main/room.html"

    def get(self, request, title):
        context = {
            "room": get_object_or_404(Room, title=title),
            "path": request.META.get("PATH_INFO").split("/")[-2]
        }
        if request.user.username != context.get("room").host.username:
            messages.error(request, "You are not authorized to perform this action")
            return redirect("main:home")

        form_initial_data = {
            "title": title,
            "topic": context.get("room").topic.name,
            "description": context.get("room").description,
        }
        context["edit_room_form"] = EditRoomForm(initial=form_initial_data)
        return render(request, self.template_name, context)
    
    def post(self, request, title):
        context = {
            "room": get_object_or_404(Room, title=title),
            "path": request.META.get("PATH_INFO").split("/")[-2]
        }

        form_initial_data = {
            "title": title,
            "topic": context.get("room").topic.name,
            "description": context.get("room").description,
        }
        
        context["edit_room_form"] = EditRoomForm(request.POST, initial=form_initial_data)
        if context.get("edit_room_form").is_valid():
            form_data = context.get("edit_room_form").cleaned_data
            context.get("room").title = form_data.get("title")
            context.get("room").topic = Topic.objects.get(name=form_data.get("topic"))
            context.get("room").description = form_data.get("description")
            context.get("room").save()
            messages.success(request, "Room Info updated successfully")
            return redirect("main:room", form_data.get("title"))
            
        return render(request, self.template_name, context)


class DeleteRoomView(View):
    temaplte_name = "main/room.html"

    def get(self, request, title):
        context = {
            "room": get_object_or_404(Room, title=title),
            "path": request.META.get("PATH_INFO").split("/")[-2],
        }
        if request.user.username != context.get("room").host.username:
            messages.error(request, "You are not authorized to perform this action")
            return redirect("main:home")
        
        return render(request, self.temaplte_name, context)
    
    def post(self, request, title):
        context = {
            "room": get_object_or_404(Room, title=title),
        }
        if Room.objects.filter(Q(topic__name__icontains=context.get("room").topic.name)).count() == 1:
            topic = Topic.objects.get(name=context.get("room").topic.name)
            topic.delete()
        
        context.get("room").delete()
        messages.success(request, "The room was deleted successfully")
        return redirect("main:home")


class EditMessageView(View):
    template_name = "main/room.html"

    def get(self, request, title, pk):
        context = {
            "room": get_object_or_404(Room, title=title),
            "msg": get_object_or_404(Message, id=pk),
            "path": request.META.get("PATH_INFO").split("/")[-2],
        }
        if request.user.username != context.get("msg").sender.username:
            messages.error(request, "You are not authorized to perform this action")
            return redirect("main:home")
        
        context["edit_msg_form"] = EditMessageForm(instance=context.get("msg"))
        return render(request, self.template_name, context)
    
    def post(self, request, title, pk):
        context = {
            "room": get_object_or_404(Room, title=title),
            "msg": get_object_or_404(Message, id=pk),
        }
        context["edit_msg_form"] = EditMessageForm(request.POST, instance=context.get("msg"))
        if context.get("edit_msg_form").is_valid():
            context.get("edit_msg_form").save()
            messages.success(request, "Your message was edited successfully")
            return redirect("main:room", title)
        
        return render(request, self.template_name, context)


class DeleteMessageView(View):
    template_name = "main/room.html"

    def get(self, request, title, pk):
        context = {
            "room": get_object_or_404(Room, title=title),
            "msg": get_object_or_404(Message, id=pk),
            "path": request.META.get("PATH_INFO").split("/")[-2],
        }
        if request.user.username != context.get("msg").sender.username:
            messages.error(request, "You are not authorized to perform this action")
            return redirect("main:home")
        
        return render(request, self.template_name, context)
    
    def post(self, request, title, pk):
        context = {
            "room": get_object_or_404(Room, title=title),
            "msg": get_object_or_404(Message, id=pk),
        }
        if Message.objects.filter(Q(room__title__icontains=title) & Q(sender__username__icontains=request.user.username)).count() == 1:
            context.get("room").participants.remove(request.user)

        context.get("msg").delete()
        messages.success(request, "Your message was deleted successfully")
        return redirect("main:room", title)