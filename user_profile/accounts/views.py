from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms.models import model_to_dict

from .models import Profile
from .forms import ProfileForm, UserForm, ChangePasswordForm


def sign_in(request):
    """Signs user in.  Uses default Django forms and models."""
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:display_account')
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    """Used for user registration.  Uses default forms and models from Django."""
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, "You're now a user! You've been signed in, too.")
            return HttpResponseRedirect(reverse('accounts:display_account'))
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    """Default sign out view."""
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_account(request):
    """Simple view to display user data and their profile."""
    current_user = request.user
    try:
        profile = Profile.objects.filter(user_id=current_user.id).get()
        return render(request, 'accounts/display_account.html', {"profile": profile})
    except:
        return render(request, 'accounts/display_account.html')



@login_required
def edit_profile(request):
    """
    View to allow user to setup or edit their profile.  Uses a user form and a profile form.
    Will write to the default django model and a custom profile model.
    """
    current_user = request.user
    user_form = UserForm(initial=model_to_dict(current_user))
    try:
        profile_attributes = Profile.objects.filter(user_id=current_user.id).get()
        profile_form = ProfileForm(initial=model_to_dict(profile_attributes))
    except:
        profile_attributes = None
        profile_form = ProfileForm()
    if request.method == 'POST':
        user_profile = UserForm(data=request.POST, instance=current_user)
        submitted_profile = ProfileForm(data=request.POST, files=request.FILES)
        if submitted_profile.is_valid() and user_profile.is_valid():
            profile = submitted_profile.save(commit=False)
            profile.user = current_user
            if len(request.FILES) == 0 and not profile_attributes:
                profile.avatar = 'chevron.svg'
            elif len(request.FILES) == 0 and profile_attributes.avatar:
                profile.avatar = profile_attributes.avatar
            profile.save()
            user_profile.save()
            return HttpResponseRedirect(reverse('accounts:display_account'))
        else:
            messages.error(request, 'Please correct the error below.')
    return render(request, 'accounts/edit_account.html', {"profile_form": profile_form, "user_form": user_form})


@login_required
def change_password(request):
    """View to update user password.  Uses default change password form."""
    form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('accounts:display_account'))
        else:
            messages.error(request, 'Please correct the error below.')
    return render(request, 'accounts/change_password.html', {'form': form})
