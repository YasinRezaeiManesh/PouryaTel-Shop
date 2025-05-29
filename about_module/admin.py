from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    pass
