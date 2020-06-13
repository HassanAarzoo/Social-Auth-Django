from django import forms

from users.models import UserDetails


class UserDetailsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserDetails
        fields = ('name', 'email_field', 'password')
