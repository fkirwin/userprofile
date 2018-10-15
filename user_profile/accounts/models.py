from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, default="")
    bio = models.TextField(null=True, default="")
    avatar = models.ImageField(upload_to='C:/TreehouseProjects/userprofile/user_profile/assets/images/', null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
