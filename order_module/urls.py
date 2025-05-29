from django.urls import path
from .views import *


urlpatterns = [
    path('add-to-order/', add_to_order, name='add_to_order'),
]
