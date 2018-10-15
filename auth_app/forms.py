from django import forms
from .models import CUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    email= forms.EmailField(required=True)

    class Meta:
        model=CUser
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class UserEditForm(UserChangeForm):

    class Meta:
        model=CUser
        fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'website',
        'password',
        )

class ProfileImgForm(forms.ModelForm):

    class Meta:
        model=CUser
        fields = (
        'profile_image',
        )
