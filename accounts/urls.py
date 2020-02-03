from django.urls import path, include

from .views import (
    DashboardView, LoginView, LogoutView, AddUserView,
    ForgotPasswordView, ResetPasswordView, ChangePasswordView,
    UsersView, EditUserView, login_token_view
)

app_name = "accounts"
urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login"),
    path("loginToken/<int:id>/", login_token_view, name="login_token"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/<reset_token>/",
         ResetPasswordView.as_view(), name="reset_password"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("users/", UsersView.as_view(), name="users"),
    path("add_user/", AddUserView.as_view(), name="add_user"),
    path("edit_user/<int:id>/", EditUserView.as_view(), name="edit_user"),

]

