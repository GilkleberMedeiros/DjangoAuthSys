from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="home_profile"),
    path('profile/login/', views.LogIn.as_view(), name="login"),
    path('profile/logout/', views.LogOut.as_view(), name="logout"),
    path('profile/signin/', views.signin, name="signin"),
]