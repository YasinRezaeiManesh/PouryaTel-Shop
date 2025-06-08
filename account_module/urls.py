from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-pass/', ForgotPasswordView.as_view(), name='forgot_pass'),
    path('reser-pass/<active_code>', ResetPasswordView.as_view(), name='reset_pass'),
]
