from django import forms
from django.core.validators import validate_email
from . import models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
#Create a “profile” view to display a user Include a link to edit the profile.


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'])
    bio = forms.CharField(min_length=10, widget=forms.Textarea)
    avatar = forms.ImageField()
    user = forms.IntegerField(widget=forms.HiddenInput, required=False)
    id = forms.IntegerField(widget=forms.HiddenInput, required=False)

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

    """
    Using inheritance to leverage existing form with altered labels for display.
    All save methods remain the same.
    """

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].label = "Current Password"
        self.fields['new_password1'].label = "New Password"
        self.fields['new_password2'].label = "Confirm Password"

