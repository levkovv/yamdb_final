from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles:
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    role_choices = (
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    )


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=UserRoles.role_choices, default='user',
        max_length=50)

    class Meta:
        ordering = ('username',)
