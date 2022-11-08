from re import template
from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField ,UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
# from django.contrib.auth.models import User 
from django import forms

User = get_user_model()

# class UserAdminChangeForm(admin_forms.UserChangeForm):
#     class Meta(admin_forms.UserChangeForm.Meta):
#         model = User


# class UserAdminCreationForm(admin_forms.UserCreationForm):
#     """
#     Form for User Creation in the Admin Area.
#     To change user signup, see UserSignupForm and UserSocialSignupForm.
#     """

#     class Meta(admin_forms.UserCreationForm.Meta):
#         model = User

#         error_messages = {
#             "username": {"unique": _("This username has already been taken.")}
#         }


class UserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name',widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name',widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

#proj_app/forms.py

class CustomUserCreationForm(UserCreationForm):
    class Meta(RegistrationForm.Meta):
    # class Meta:
            model = User
            fields = ('email','username',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
            model = User
            fields = ('email',  'username',)

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

