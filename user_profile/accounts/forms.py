from django import forms
from django.core.validators import validate_email
from django.contrib.auth.forms import PasswordChangeForm
from django.http import QueryDict


from . import models


class ProfileForm(forms.ModelForm):
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
    first_name = forms.CharField(min_length=1)
    last_name = forms.CharField(min_length=1)
    email = forms.EmailField(max_length=254, validators=[validate_email])

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

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email"]


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
