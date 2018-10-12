from django import forms

from . import models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

#Create a “profile” view to display a user Include a link to edit the profile.

class ProfileForm(UserCreationForm):
    class Meta:
        model = models.Profile
        fields = ['username',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name',
                  'email',
                  'date_of_birth',
                  'bio',
                  'avatar']
