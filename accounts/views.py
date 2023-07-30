from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy


class LoggedOut(LogoutView):
    template_name = "account/logged_out.html"


# class LocalPasswordReset(PasswordResetView):
#     template_name = "account/password_reset_form.html"
#     email_template_name = "account/password_reset_email.html"
#     success_url = reverse_lazy("local_password_reset_done")


# class LocalPasswordResetDone(PasswordResetDoneView):
#     template_name = "account/password_reset_done.html"


# class LocalPasswordResetConfirm(PasswordResetConfirmView):
#     template_name = "account/password_reset_confirm.html"
#     success_url = reverse_lazy("local_password_reset_complete")


# class LocalPasswordResetComplete(PasswordResetCompleteView):
#     template_name = "account/password_reset_complete.html"
