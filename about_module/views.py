from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


# Create your views here.


class AboutView(TemplateView):
    template_name = 'about_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = {
            'about': Info.objects.all().first()
        }
        return context


class ContactView(TemplateView):
    template_name = 'about_module/contact.html'

    def get_context_data(self, **kwargs):
        context = {
            'contact': Contact.objects.all().first(),
            "info": Info.objects.all().first()
        }
        return context
