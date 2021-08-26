from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from colossus.apps.accounts.forms import UserForm

from .models import User
from .forms import RegistrationForm


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


def registration_form(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            User = get_user_model()

            check_user = User.objects.filter(Q(username=username) | Q(email=email))
            print(check_user.count())

            if check_user.count() !=0:
                return render(
                    request,
                    'registration/registeration_form.html',
                    {
                        'form': form,
                        'fail': "Username or Email Already Exist"
                    }
                )

            user = User.objects.create(
                username=username,
                password=make_password(password),
                email=email
            )
            user.first_name = first_name
            user.last_name = last_name
            user.is_admin = True
            user.is_staff = True
            user.save()
            print("Saved")
            return render(
                request,
                'registration/registeration_form.html',
                {
                    'form': form,
                    'success': "User Created Successfully"
                }
            )
    else:
        form = RegistrationForm()
        return render(
            request,
            'registration/registeration_form.html',
            {
                'form': form
            }
        )
