from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterUsersForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name',  'last_name', 'username', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_active = False
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


