from django.urls import path, include

from . import views

urlpatterns = [
    path("", include("allauth.urls")),
    path("password/reset/", include("allauth.urls")),
    path("loggedout/", views.LoggedOut.as_view(), name="logged_out"),
    # path(
    #     "password_reset/",
    #     views.LocalPasswordReset.as_view(),
    #     name="local_password_reset",
    # ),
    # path(
    #     "password_reset/done/",
    #     views.LocalPasswordResetDone.as_view(),
    #     name="local_password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     views.LocalPasswordResetConfirm.as_view(),
    #     name="local_password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     views.LocalPasswordResetComplete.as_view(),
    #     name="local_password_reset_complete",
    # ),
]
