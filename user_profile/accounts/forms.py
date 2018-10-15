from django import forms
from django.core.validators import validate_email
from . import models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
#Create a “profile” view to display a user Include a link to edit the profile.


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'])
    bio = forms.CharField(min_length=10, widget=forms.Textarea)
    avatar = forms.ImageField()

    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id

    def save(self, commit=True, user_id=None):
        if not user_id:
            raise forms.ValidationError("User must be logged in to make changes.")
        else:
            self.user_id = user_id
            return super().save(commit=commit)

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


