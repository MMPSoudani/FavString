from django.db import models
from datetime import datetime


class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    is_super = models.BooleanField(default=False)
    joined_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username


class AuthUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_authenticated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username}"


class String(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    string = models.TextField()
    weight = models.IntegerField(blank=True, null=True, default=0)
    favored_by = models.ManyToManyField(User, related_name="favored_by")
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.string[:20]}"
    

    class Meta:
        ordering = ["-created"]