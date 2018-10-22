import os

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=True, default="")
    bio = models.TextField(null=True, default="")
    avatar = models.ImageField(upload_to=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/assets/images/', null=True, blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
