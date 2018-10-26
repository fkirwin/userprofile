from django import forms
from django.core.validators import validate_email
from django.contrib.auth.forms import PasswordChangeForm
from django.http import QueryDict


from . import models


class ProfileForm(forms.ModelForm):
    """
    Profile form used to get values for the user's profile.
    Overrides default ModelForm constructor to strip unescessary values during initializing.
    This will prevent validation errors and allow for multiple forms to be used in the same request.
    """
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'])
    bio = forms.CharField(min_length=10, widget=forms.Textarea)
    avatar = forms.ImageField(required=False)
    user = forms.IntegerField(widget=forms.HiddenInput, required=False)
    id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', None)
        cleaned_data = {}
        if data:
            stripped_kwargs = kwargs
            for k, v in kwargs.get('data').items():
                if k in ProfileForm.declared_fields.keys() or k == 'csrfmiddlewaretoken':
                    cleaned_data.update({k: v})
            qdict = QueryDict('', mutable=True)
            qdict.update(cleaned_data)
            stripped_kwargs['data'] = qdict
            super().__init__(*args, **stripped_kwargs)
        else:
            super().__init__(*args, **kwargs)

    class Meta:
        model = models.Profile
        fields = ['date_of_birth', 'bio', 'avatar']


class UserForm(forms.ModelForm):
    """
    User form used to get values for the user's profile separate from creating an account.
    Overrides default ModelForm constructor to strip unescessary values during initializing.
    This will prevent validation errors and allow for multiple forms to be used in the same request.
    """
    first_name = forms.CharField(min_length=1)
    last_name = forms.CharField(min_length=1)
    email = forms.EmailField(max_length=254, validators=[validate_email])
    confirm_email = forms.EmailField(
        label="Confirm e-mail",
        required=True,
        help_text=("Enter the same email as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', None)
        cleaned_data = {}
        if data:
            stripped_kwargs = kwargs
            for k, v in kwargs.get('data').items():
                if k in UserForm.declared_fields.keys() or k == 'csrfmiddlewaretoken':
                    cleaned_data.update({k: v})
            qdict = QueryDict('', mutable=True)
            qdict.update(cleaned_data)
            stripped_kwargs['data'] = qdict
            super().__init__(*args, **stripped_kwargs)
        else:
            super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('confirm_email')
        if email != verify:
            raise forms.ValidationError("The emails you entered do not match!  Please fix your entry.")

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email", "confirm_email"]


class ChangePasswordForm(PasswordChangeForm):

    """
    Using inheritance to leverage existing form with altered labels for display.
    All save methods remain the same.
    Additional validators have been added to settings to ensure password safety and strength.
    """

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].label = "Current Password"
        self.fields['new_password1'].label = "New Password"
        self.fields['new_password2'].label = "Confirm Password"

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password1')
        if old_password == new_password:
            raise forms.ValidationError('Old password and new password should not match.')
