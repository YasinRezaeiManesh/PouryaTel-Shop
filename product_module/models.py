from django.db import models
from django_jalali.db import models as jalali_models
from account_module.models import User


# Create your models here.

class MobileCompany(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    url_address = models.SlugField(verbose_name='عنوان در url', max_length=100, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'شرکت'
        verbose_name_plural = 'شرکت های موبایل'

    def __str__(self):
        return self.name


class Attachments(models.Model):
    name = models.CharField(max_length=50)
    url_address = models.SlugField(verbose_name='عنوان در url', max_length=100, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'گروه'
        verbose_name_plural = 'دسته بندی لوازم جانبی'

    def __str__(self):
        return self.name


class ProductCategories(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام')
    url_title = models.SlugField(max_length=100, unique=True, verbose_name='نام در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    image = models.ImageField(upload_to='images/product_cat_images', blank=True, null=True, verbose_name='تصویر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام محصول')
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    attachment = models.ForeignKey(Attachments, verbose_name='دسته بندی در لوازم جانبی', on_delete=models.CASCADE, null=True,
                                   blank=True)

    is_mobile = models.BooleanField(verbose_name='موبایله؟', default=False)
    mobile_company = models.ForeignKey(MobileCompany, verbose_name='شرکت موبایل', on_delete=models.CASCADE, null=True,
                                       blank=True)
    ram = models.CharField(max_length=100, verbose_name='مقدار رام', null=True, blank=True)
    memory = models.CharField(max_length=100, verbose_name='مقدار حافظه', null=True, blank=True)
    image = models.ImageField(upload_to='images/product_images', verbose_name='تصویر')
    inventory = models.BooleanField(verbose_name='موجودی', default=True)
    slug = models.SlugField(unique=True, db_index=True, null=True, blank=True, verbose_name='عنوان در url',
                            max_length=100)
    off = models.BooleanField(verbose_name='تخفیف خورده', default=False)
    perc_off = models.IntegerField(verbose_name='درصد تخفیف', default=0)
    off_price = models.IntegerField(verbose_name='قیمت تخفیف خورده', null=True, blank=True)
    sub_cat = models.ForeignKey(ProductCategories, verbose_name='دسته بندی', null=True, blank=True,
                                on_delete=models.CASCADE, related_name='product_sub_cat')
    colors = models.CharField(max_length=200, verbose_name='رنگ های موجود', default='')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    parent = models.ForeignKey('ProductComments', verbose_name='والد', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='کامنت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    date = jalali_models.jDateField(auto_now_add=True, verbose_name='تاریخ شمسی')
    success = models.BooleanField(default=False, verbose_name='تایید شده')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
