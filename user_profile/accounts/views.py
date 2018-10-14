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
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:display_account')  # TODO: go to profile
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
            messages.success(request,"You're now a user! You've been signed in, too.")
            return HttpResponseRedirect(reverse('accounts:display_account'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


def display_account(request):
    current_user = request.user
    try:
        current_user_attributes = Profile.objects.get(pk=current_user)
        profile_form = ProfileForm(initial= model_to_dict(current_user_attributes))
        user_form = UserForm(initial=model_to_dict(current_user))
        if request.method == 'POST':
            profile_form = ProfileForm(data=request.POST)
            user_form = UserForm(data=request.POST)
            if profile_form.is_valid():
                profile_form.save()
                user_form.save()
                return HttpResponseRedirect(reverse('accounts:display_account'))
        return render(request, 'accounts/display_account.html', {"user": current_user_attributes, "profile_form":profile_form, "user_form":user_form})
    except:
        profile_form = ProfileForm()
        user_form = UserForm(initial=model_to_dict(current_user))
        if request.method == 'POST':
            profile_form = ProfileForm(data=request.POST)
            user_form = UserForm(data=request.POST)
            if profile_form.is_valid():
                profile_form.save()
                user_form.save()
                return HttpResponseRedirect(reverse('accounts:display_account'))
        return render(request, 'accounts/display_account.html', {"profile_form": profile_form, "user_form": user_form})



@login_required
def edit_profile(request):
    current_user = request.user
    try:
        current_user_attributes = Profile.objects.get(pk=current_user)
        profile_form = ProfileForm(initial=model_to_dict(current_user_attributes))
        user_form = UserForm(initial=model_to_dict(current_user))
        if request.method == 'POST':
            profile_form = ProfileForm(data=request.POST, files=request.avatar)
            user_form = UserForm(data=request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                user_form.save()
                return HttpResponseRedirect(reverse('accounts:display_account'))
        return render(request, 'accounts/edit_account.html',
                      {"user": current_user_attributes, "profile_form": profile_form, "user_form": user_form})
    except:
        profile_form = ProfileForm()
        user_form = UserForm(initial=model_to_dict(current_user))
        if request.method == 'POST':
            profile_form = ProfileForm(data=request.POST, files=request.FILES)
            user_form = UserForm(data=request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.fields['user_id']=current_user
                profile_form.save()
                user_form.save()
                return HttpResponseRedirect(reverse('accounts:display_account'))
            else:
                print(profile_form.errors)
                print(profile_form.data)
                print(request.POST)
        return render(request, 'accounts/edit_account.html', {"profile_form": profile_form, "user_form": user_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            HttpResponseRedirect(reverse('accounts:display_account'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})