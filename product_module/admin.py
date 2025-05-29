from django.contrib import admin

from product_module.models import *


# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory', 'off']


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategories)
class ProductCategoriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'url_title']


@admin.register(MobileCompany)
class MobileCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Attachments)
class AttachmentsAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductComments)
class ProductCommentsAdmin(admin.ModelAdmin):
    pass

