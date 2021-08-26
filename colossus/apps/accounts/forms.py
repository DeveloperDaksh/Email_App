from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

import pytz

from .models import User


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    TIMEZONE_CHOICES = (('', '---------'),) + tuple(map(lambda tz: (tz, tz), pytz.common_timezones))

    timezone = forms.ChoiceField(
        choices=TIMEZONE_CHOICES,
        required=False,
        label=_('Timezone')
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'timezone')


class RegistrationForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
