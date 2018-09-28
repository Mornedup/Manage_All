from django.shortcuts import render, redirect
from authapp.forms import RegistrationForm, UserEditForm, ProfileImgForm
from .models import CUser
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, login as auth_login
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('homepage')

    form = AuthenticationForm(request)
    return render(request, 'authapp/login.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')

    form = RegistrationForm()
    return render(request, 'authapp/register.html', {'form': form})

@login_required
def view_profile(request):
    if request.method == 'POST':
        PrflImgForm = ProfileImgForm(request.POST, request.FILES, instance=request.user)
        if PrflImgForm.is_valid():
            PrflImgForm.save()
            return redirect('view_profile')

    PrflImgForm = ProfileImgForm(instance=request.user)
    args = {'user': request.user, 'PrflImgForm': PrflImgForm}
    return render(request, 'authapp/profile.html', args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        Userform = UserEditForm(request.POST, instance=request.user)
        if (Userform.is_valid()):
            Userform.save()
            return redirect('view_profile')

    else:
        Userform = UserEditForm(instance=request.user)
        args = {'Userform': Userform}
        return render(request, 'authapp/edit_profile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=form.user)
            return redirect('view_profile')

    else:
        form = PasswordChangeForm(user=request.user)

    args = {'form': form}
    return render(request, 'authapp/change_password.html', args)
