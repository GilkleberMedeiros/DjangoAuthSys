from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.Profile.as_view(), name="profile"),
    path('change/done/', views.ChangeDone.as_view(), name="profile_changes_done"),
    path('confirm/email/', views.ConfirmEmail.as_view(), name="confirm_email"),
    path('send/validation/email/', views.SendValidationEmail.as_view(), name="send_validation_email"),
    path('validation/email/sent/', views.ValidationEmailSent.as_view(), name="validation_email_sent"),
    path('password/reset/', views.PasswordReset.as_view(), name="password_reset"),
    path('password/reset/done/', views.PasswordResetDone.as_view(), name="password_reset_done"),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', views.PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path('password/reset/complete/', views.PasswordResetComplete.as_view(), name="password_reset_complete"),
    path('login/', views.LogIn.as_view(), name="login"),
    path('logout/', views.LogOut.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
]