from django.urls import path
from .views import *


urlpatterns = [
    path('about-us/', AboutView.as_view(), name='about_us'),
    path('contact-us/', ContactView.as_view(), name='contact_us'),
]
