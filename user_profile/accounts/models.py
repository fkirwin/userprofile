from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(User):
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
