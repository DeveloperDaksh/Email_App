from django import forms


class EmailForms(forms.Form):
    email_default = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Default Email'}))
    email_server = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email Server'}))
    email_backend = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email Backend'}))
    email_host = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email Host'}))
    email_port = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email Port'}))
    email_host_user = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email Host User'}))
    email_host_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Email Host Password'}))
    email_default_text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Default Text'}))


class PhoneBookForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
