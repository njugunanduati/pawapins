import jwt
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.auth.models import User

from accounts.models import Profile
from accounts.utils import reset_password_token
from accounts.emails import send_forgot_password_request, send_change_password


class AddUserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = (
            "email", "first_name", "last_name",
            "password1", "password2","username"
        )



class ForgotPasswordForm(forms.Form):

    email = forms.EmailField()

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data["email"]).first()
        if not user:
            raise forms.ValidationError("Invalid email address.")

        if not user.is_active:
            raise forms.ValidationError("Please activate your account.")

        return user.email

    def clean(self):
        email = self.cleaned_data.get("email")
        if email:
            user = User.objects.filter(email=email).first()
            profile = Profile.objects.filter(
                user=user).first()
            profile.generate_password_request_date()
            profile.reset_password_token = reset_password_token(user.email)
            profile.save()

            send_forgot_password_request(
                profile.user, profile.reset_password_token)
        else:
            raise forms.ValidationError("Unable to reset your password.")

        return self.cleaned_data



class LoginForm(forms.Form):

    username = forms.CharField(
        label="Username",
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )


class ResetPasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.reset_token = kwargs.pop("reset_token", None)
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
		

        if password1 != password2:
            raise forms.ValidationError("Passwords didn't match.")

        profile = Profile.objects.filter(
            reset_password_token=self.reset_token).select_related("user").first()

        if not profile:
            raise forms.ValidationError("Invalid or expired token.")

        profile.reset_password_token = None
        profile.reset_password_request_date = None
        profile.user.set_password(self.cleaned_data["password1"])

        profile.user.save()
        profile.save()

        send_change_password(profile.user)


        return self.cleaned_data



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords didn't match.")

        return self.cleaned_data
