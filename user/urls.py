
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginApiView.as_view(), name='login'), #userapp urls
    path('register', views.UserRegisterApiView.as_view(), name='register')
]
