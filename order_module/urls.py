from django.urls import path
from .views import *


urlpatterns = [
    path('add-to-order/', add_to_order, name='add_to_order'),
    path('request-payment/', request_payment, name='request_payment'),
    path('verify-payment/', verify_payment, name='verify_payment'),
]
