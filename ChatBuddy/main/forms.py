from django import forms
from .models import User, Profile, Topic, Room, Message
from re import compile


class LoginForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered")
        return email


class RegisterForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    username = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password_1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password_2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        # labels = {
        #     "full_name": "",
        #     "birth_date": "",
        #     "bio": "",
        #     "avatar": "",
        # }
        widgets = {
            "user": forms.HiddenInput(),
            "full_name": forms.TextInput(),
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"class": "h-24"}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Search the website",
        "class": "bg-gray-600 focus:bg-white focus:outline-none border border-gray-400 rounded-lg py-2 px-4 text-xl text-center w-full"}))


class CreateRoomForm(forms.Form):
    topic = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Topic"}))
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Title"}))
    description = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={"placeholder": "Room description..."}))

    def clean_topic(self):
        topic = self.cleaned_data.get("topic").lower()
        if not Topic.objects.filter(name=topic).exists():
            Topic.objects.create(name=topic)
        return topic
    
    def clean_title(self):
        title = self.cleaned_data.get("title").lower()
        if Room.objects.filter(title=title).exists():
            raise forms.ValidationError("This room already exists")
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description == "":
            return "No description is available"
        return description


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        labels = {
            "body": "",
        }
        widgets = {
            "room": forms.HiddenInput(),
            "sender": forms.HiddenInput(),
            "body": forms.Textarea(attrs={"placeholder": "Type your message...",
                "class": "border rounded-lg w-8/12 py-2 px-3 h-24 focus:outline-none"}),
        }


class EditRoomForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Title",
        "class": "w-10/12 mb-3 px-2 py-3 rounded-lg"}))
    topic = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Topic",
        "class": "w-10/12 mb-3 px-2 py-3 rounded-lg"}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Description",
        "class": "w-10/12 h-24 px-2 py-3 rounded-lg"}))
    
    def clean_title(self):
        title = self.cleaned_data.get("title").lower()
        if "title" in self.changed_data:
            if Room.objects.filter(title=title).exists():
                raise forms.ValidationError("This room already exists")
        return title
    
    def clean_topic(self):
        topic = self.cleaned_data.get("topic").lower()
        if "topic" in self.changed_data:
            if not Topic.objects.filter(name=topic).exists():
                Topic.objects.create(name=topic)
        return topic


class EditMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        labels = {
            "body": "",
        }
        widgets = {
            "body": forms.Textarea(attrs={"placeholder": "Edit your message...",
                "class": "border rounded-lg w-8/12 py-2 px-3 h-24"}),
        }