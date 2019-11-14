import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import logout, update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Profile
from .forms import (
    AddUserForm, ForgotPasswordForm, ResetPasswordForm,
    ChangePasswordForm, LoginForm)
from .emails import send_forgot_password_request, send_change_password

        

class LoginView(TemplateView):
    template_name = "login.html"
    form = LoginForm
    title = 'Login'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if "form" not in kwargs:
            context["form"] = self.form
            context["title"] = self.title

        return context

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password']
            )
            if user:
                if user.is_active is True:
                    print(user)
                    login(request, user)
                    messages.success(request, "Successfully logged in. Welcome "+ user.email)
                    return HttpResponseRedirect(reverse("accounts:dashboard"))
                else:
                    messages.warning(request, "User inactive. Talk to admin")
                    return HttpResponseRedirect(reverse("accounts:login"))
            else:        
                messages.error(request, "Wrong credentials")
                return HttpResponseRedirect(reverse("accounts:login"))
        messages.error(request, "Wrong credentials")
        return HttpResponseRedirect(reverse("accounts:login"))


class AddUserView(TemplateView):
    template_name = "add_user.html"
    form = AddUserForm
    title = 'Add User'

    def get_context_data(self, **kwargs):
        context = super(AddUserView, self).get_context_data(**kwargs)
        if "form" not in kwargs:
            common = CommonPasswordValidator()
            context["form"] = self.form
            context["title"] = self.title
            context["passwords"] = json.dumps(list(common.passwords))

        return context

    def post(self, request):
        form = AddUserForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            profile = Profile(
                phone_number = form.cleaned_data["phone_number"],
                user = user
            )
            profile.save()

            messages.success(
                request, "Successfully signed up. Check your email for conformation link.")
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            messages.error(request, "Please fix the errors.")
            return self.render_to_response(self.get_context_data(
                form=form,
            ))


class ForgotPasswordView(TemplateView):
    template_name = "forgot_password.html"
    form = ForgotPasswordForm

    def get_context_data(self, **kwargs):
        context = super(ForgotPasswordView, self).get_context_data(**kwargs)
        context["form"] = self.form
        context["title"] = 'Forgot Password'
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse(reverse("accounts:dashboard")))
        return self.render_to_response(self.get_context_data())

    def post(self, request):
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            messages.success(
                request, "Please check your email for instructions.")
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return self.render_to_response(self.get_context_data(
                form=form,
            ))


class ResetPasswordView(TemplateView):
    template_name = "reset_password.html"
    form = ResetPasswordForm
    token = None

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        if "form" not in kwargs:
            context["form"] = self.form
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse(reverse("accounts:dashboard")))
        return self.render_to_response(self.get_context_data())

    def post(self, request, reset_token):
        form = ResetPasswordForm(data=request.POST, reset_token=reset_token)
        if form.is_valid():
            messages.success(request, "Password changed successfully.")
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return self.render_to_response(self.get_context_data(
                form=form,
            ))


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    title = 'Dashboard'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context["title"] = self.title
        return context



class ChangePasswordView(LoginRequiredMixin, View):

    def post(self, request):
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            if user.check_password(data["old_password"]):
                user.set_password(data["password1"])
                user.save()

                update_session_auth_hash(request, user)

                messages.success(request, "Password changed successfully.")
            else:
                messages.error(request, "Invalid password provided.")

        return HttpResponseRedirect(reverse("accounts:profile"))


class UsersView(LoginRequiredMixin, TemplateView):
    template_name = "users.html"
    title = 'Users'

    def get_context_data(self, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        context["users"] = User.objects.all()
        context["title"] = self.title
        return context


class EditUserView(TemplateView):
    template_name = "user.html"
    form = AddUserForm
    title = 'Edit User'

    def get_context_data(self, **kwargs):
        context = super(EditUserView, self).get_context_data(**kwargs)
        if "form" not in kwargs:
            common = CommonPasswordValidator()
            context["form"] = self.form(instance=self.request.user)
            context["title"] = self.title
            context["passwords"] = json.dumps(list(common.passwords))

        return context

    def post(self, request, id):
        print("request", request)
        form = AddUserForm(data=request.POST, instance=self.request.user)

        if form.is_valid():
            user = form.save(commit=False)
            # load the profile instance created by the signal
            user.profile.phone_number = form.cleaned_data["phone_number"]
            user.is_active = True
            user.save()

            messages.success(
                request, "User details successfully updated.")
            return HttpResponseRedirect(reverse("accounts:users"))
        else:
            messages.error(request, "Please fix the errors.")
            return self.render_to_response(self.get_context_data(
                form=form,
            ))


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("accounts:login"))
