from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserRole


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=100, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=100, required=True, help_text='Required. Enter your last name.')
    bio = forms.Textarea()
    role = forms.ChoiceField(choices=UserRole.choices, required=True, help_text='Required. Select a user role.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'bio', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.role == UserRole.MANAGER:
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True, help_text='Required. Enter your registered email address.')
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Required. Enter your password.')


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=100, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=100, required=True, help_text='Required. Enter your last name.')
    bio = forms.Textarea()
    role = forms.ChoiceField(choices=UserRole.choices, required=True, help_text='Required. Select a user role.')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'bio', 'role')


