from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.Profile.as_view(), name="profile"),
    path('change/done/', views.ChangeDone.as_view(), name="profile_changes_done"),
    path('login/', views.LogIn.as_view(), name="login"),
    path('logout/', views.LogOut.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
]