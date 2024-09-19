from django.contrib import admin
from django.urls import path,include
from authentication import views

# app_name='auth'

urlpatterns = [
    path('register/', views.UserSignUpView.as_view(),name='register'),
    path('login/', views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
]