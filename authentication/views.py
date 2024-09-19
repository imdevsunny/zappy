from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib import messages
from django.views.generic import View
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
# from payments.models import UserSubscriptions
from django.conf import settings
# import stripe
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.encoding import smart_str
import json
from django.contrib.auth import get_backends

CustomUser = get_user_model()


class UserSignUpView(View):
    def get(self, request, *args, **kwargs):
        context={}
        return render(request, "signup.html", context)

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password1", "").strip()
            confirm_password = request.POST.get("password2", "").strip()

            if not email or not password or not confirm_password:
                messages.error(request, "All fields are required.")
                return redirect('register')

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('register')

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('register')

            with transaction.atomic():
                user = CustomUser.objects.create_user(email=email, password=password)
                user.subscribed = True
                user.save()
                backend = get_backends()[0]  # Select the appropriate backend here
                user.backend = backend.__module__ + '.' + backend.__class__.__name__
                login(request, user)
                messages.success(request, "Subscription Added Successfully.")
                return redirect('home')
                
        except Exception as e:
            print(str(e))
            messages.error(request, "Something went wrong.")
            return redirect('home')

class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "login.html", {})

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST.get("email","").rstrip()
            password = request.POST.get("password1","").rstrip()


            if not email or not password:
                messages.error(request, "Email and password are required.")
                return redirect("login")
            
            user = CustomUser.objects.filter(email=email).first()
            
            if not user:
                messages.error(request, "Email not Registered.")
                return redirect("home")
            
            if user.check_password(password):
                backend = get_backends()[0]  # Select the appropriate backend here
                user.backend = backend.__module__ + '.' + backend.__class__.__name__
                login(request, user)
                messages.success(request, "Login successful.")
                if not user.subscribed:
                    messages.info(request, "Please subscribe to access services")
                    return redirect('register')
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password.")
                return redirect("login")
        except Exception as e:
            messages.error(request, f"{str(e)}")
            return redirect("login")


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            logout(request)
            messages.success(request, "Logout successful.")
            return redirect("login")
        except:
            return render(request, "login.html", {})