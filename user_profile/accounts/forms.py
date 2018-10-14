from django import forms
from django.core.validators import validate_email
from . import models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
#Create a “profile” view to display a user Include a link to edit the profile.


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'])
    bio = forms.CharField(min_length=10)
    avatar = forms.ImageField()
    user = forms.

    class Meta:
        model = models.Profile
        fields = ['date_of_birth',
                  'bio',
                  'avatar']

class UserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, validators=[validate_email])
    class Meta:
        model = models.User
        fields = ["first_name",
                  "last_name",
                   "email"]

class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].label = "Current Password"
        self.fields['new_password1'].label = "New Password"
        self.fields['new_password2'].label = "Confirm Password"


