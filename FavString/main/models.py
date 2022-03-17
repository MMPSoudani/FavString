from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=30)
    is_super = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username


class String(models.Model):
    string = models.TextField()
    weight = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.string[:20]}"
    

    class Meta:
        ordering = ["-updated", "-created"]


class FavoriteString(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strings = models.ManyToManyField(String, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s favorite strings"