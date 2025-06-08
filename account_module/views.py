from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.utils.crypto import get_random_string
from .forms import *
from .models import User
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, logout
from utils.email_service import send_email


# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_first_name = register_form.cleaned_data.get('first_name')
            user_last_name = register_form.cleaned_data.get('last_name')
            user_email = register_form.cleaned_data.get('email')
            user_phone = register_form.cleaned_data.get('phone')
            user_password = register_form.cleaned_data.get('password')
            user_e: bool = User.objects.filter(email__iexact=user_email).exists()
            user_p: bool = User.objects.filter(number__iexact=user_phone).exists()

            if user_e:
                register_form.add_error('email', 'ایمیل وارد شده تکراری میباشد')
            elif user_p:
                register_form.add_error('phone', 'شماره تلفن وارد شده تکراری میباشد')
            else:
                new_user = User(
                    first_name=user_first_name,
                    last_name=user_last_name,
                    email=user_email,
                    email_active_code=get_random_string(48),
                    is_active=True,
                    number=user_phone,
                    username=user_email,
                )
                new_user.set_password(user_password)
                new_user.save()
                return redirect(reverse('home_page'))

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user:
                is_current_password = user.check_password(user_password)
                if is_current_password:
                    login(request, user)
                    return redirect(reverse('home_page'))
                else:
                    login_form.add_error('password', 'کلمه عبور وارد شده نادرست است')
            else:
                login_form.add_error('email', 'شما حساب کاربری ندارید')
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home_page'))


class ForgotPasswordView(View):
    def get(self, request: HttpRequest):
        forgot_form = ForgotPasswordForm()
        context = {
            'forgot_form': forgot_form
        }
        return render(request, 'account_module/forgot_page.html', context)

    def post(self, request: HttpRequest):
        forgot_form = ForgotPasswordForm(request.POST)
        if forgot_form.is_valid():
            user_email = forgot_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'email/forgot_password.html')
                return redirect(reverse('home_page'))
            else:
                forgot_form.add_error('email', 'ایمیل وارد شده وجود ندارد')
        context = {
            'forgot_form': forgot_form
        }
        return render(request, 'account_module/forgot_page.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        reset_form = ResetPasswordForm()
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('home_page'))
        context = {
            'reset_form': reset_form,
            'user': user
        }
        return render(request, 'account_module/reset_page', context)

    def post(self, request: HttpRequest, active_code):
        reset_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_form.is_valid():
            if user is None:
                return redirect(reverse('home_page'))
            else:
                new_password = reset_form.cleaned_data.get('new_password')
                user.set_password(new_password)
                user.email_active_code = get_random_string(48)
                user.save()
                return redirect(reverse('login'))
        context = {
            'reset_form': reset_form,
            'user': user
        }
        return render(request, 'account_module/reset_page', context)
