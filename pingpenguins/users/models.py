from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=50, blank=True, null=True) 
    position = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    tenure = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    sticky_note_colour = models.CharField(max_length=20, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username