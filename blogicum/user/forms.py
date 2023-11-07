from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

USER = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = USER
        fields = ('username', 'email')


class CustomUserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta(UserChangeForm.Meta):
        model = USER
        fields = ('username', 'email', 'first_name', 'last_name')
        exclude = ('password',)
