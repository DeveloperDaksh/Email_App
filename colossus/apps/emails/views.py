from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from decouple import config
from django.db.models import Q
import os

from .forms import EmailForms, PhoneBookForm
from .models import EmailUsers, PhoneBook


@login_required
def get_email_details(request):
    if request.method == 'POST':
        form = EmailForms(request.POST)
        if form.is_valid():
            email_default = form.cleaned_data['email_default']
            email_server = form.cleaned_data['email_server']
            email_backend = form.cleaned_data['email_backend']
            email_host = form.cleaned_data['email_host']
            email_port = form.cleaned_data['email_port']
            email_host_user = form.cleaned_data['email_host_user']
            email_host_password = form.cleaned_data['email_host_password']
            email_default_text = form.cleaned_data['email_default_text']
            user = request.user
            try:
                email_detail = EmailUsers.objects.get(user=user)
                email_detail.email_default = email_default
                email_detail.email_server = email_server
                email_detail.email_backend = email_backend
                email_detail.email_host = email_host
                email_detail.email_port = email_port
                email_detail.email_host_user = email_host_user
                email_detail.email_host_password = make_password(email_host_password)
                email_detail.email_default_text = email_default_text
                email_detail.save()
            except EmailUsers.DoesNotExist:
                email_details = EmailUsers.objects.create(
                    user=user,
                    email_default=email_default,
                    email_host_user=email_host_user,
                    email_host_password=make_password(email_host_password),
                    email_server=email_server,
                    email_backend=email_backend,
                    email_port=email_port,
                    email_host=email_host,
                    email_default_text=email_default_text
                )
                email_details.save()

            os.environ["DEFAULT_FROM_EMAIL"] = email_default
            os.environ["SERVER_EMAIL"] = email_server
            os.environ["EMAIL_BACKEND"] = email_backend
            os.environ["EMAIL_HOST"] = email_host
            os.environ["EMAIL_PORT"] = email_port
            os.environ["EMAIL_HOST_USER"] = email_host_user
            os.environ["EMAIL_HOST_PASSWORD"] = email_host_password
            os.environ["EMAIL_USE_TLS"] = "True"
            print(config('SERVER_EMAIL'))
            return render(
                request,
                'emails/email_setup.html',
                {
                    'form': form,
                    'success': 'Email Settings  Are Configred'
                }
            )

    else:
        email_form = EmailForms()
        return render(
            request,
            'emails/email_setup.html',
            {
                'menu': 'emails',
                'form': email_form
            }
        )


@login_required
def get_phonebook(request):
    if request.method == 'POST':
        form = PhoneBookForm(request.POST)
        if form.is_valid():
            user = request.user
            email = form.cleaned_data['email']

            check_phone_book = PhoneBook.objects.filter(Q(user=user) & Q(email=email))
            print(check_phone_book.count())
            phonebook_details = PhoneBook.objects.filter(user=request.user)
            form = PhoneBookForm()
            if check_phone_book.count() > 0:
                return render(
                    request,
                    'emails/phonebook_setup.html',
                    {
                        'menu': 'phonebook',
                        'fail': 'Email Already Added',
                        'form': form,
                        'phonebook_details': phonebook_details
                    }
                )
            phonebook = PhoneBook.objects.create(
                user=user,
                email=email
            )
            phonebook.save()
            print(phonebook_details.count())
            if phonebook_details.count() > 0:
                for detail in phonebook_details:
                    print(detail.email)
                return render(
                    request,
                    'emails/phonebook_setup.html',
                    {
                        'menu': 'phonebook',
                        'success': 'Email Added',
                        'form': form,
                        'phonebook_details': phonebook_details
                    }
                )
            else:
                return render(
                    request,
                    'emails/phonebook_setup.html',
                    {
                        'menu': 'phonebook',
                        'form': form,
                        'no_data': "Currently You Don't have any Emails"
                    }
                )

    else:
        phonebook_form = PhoneBookForm()
        phonebook_details = PhoneBook.objects.filter(user=request.user)
        print(phonebook_details)
        print(phonebook_details.count())
        if phonebook_details.count() > 0:
            for detail in phonebook_details:
                print(detail.email)
            return render(
                request,
                'emails/phonebook_setup.html',
                {
                    'menu': 'phonebook',
                    'form': phonebook_form,
                    'phonebook_details': phonebook_details
                }
            )
        else:
            return render(
                request,
                'emails/phonebook_setup.html',
                {
                    'menu': 'phonebook',
                    'form': phonebook_form,
                    'no_data': "Currently You Don't have any Emails",
                }
            )
