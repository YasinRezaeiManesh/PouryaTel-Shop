from django.db import models


# Create your models here.


class Contact(models.Model):
    mobile = models.CharField(verbose_name='موبایل', max_length=11)
    email = models.EmailField(verbose_name='ایمیل', null=True, blank=True, max_length=100)
    telegram = models.CharField(verbose_name='تلگرام', null=True, blank=True, max_length=100)
    whatsapp = models.CharField(verbose_name='واتساپ', null=True, blank=True, max_length=100)
    instagram = models.CharField(verbose_name='اینستاگرام', null=True, blank=True, max_length=100)

    class Meta:
        verbose_name = 'شبکه'
        verbose_name_plural = 'تماس با ما'

    def __str__(self):
        return 'اطلاعات'


class Info(models.Model):
    site_name = models.CharField(verbose_name='اسم سایت', max_length=100)
    site_logo = models.ImageField(verbose_name='لوگو', upload_to='images/info', null=True, blank=True)
    pic_1 = models.ImageField(verbose_name='تصویر یک', upload_to='images/info')
    pic_2 = models.ImageField(verbose_name='تصویر دو', upload_to='images/info')
    description_1 = models.TextField(verbose_name='توضیحات اول')
    title_2 = models.CharField(verbose_name='عنوان دوم', max_length=100)
    description_2 = models.TextField(verbose_name='توضیحات دوم')
    address = models.TextField(verbose_name='آدرس', default='')
    work_zone = models.CharField(verbose_name='ساعت کاری', default='', max_length=100)
    copy_right = models.CharField(verbose_name='متن کپی رایت', max_length=100, default='')

    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'درباره ما'

    def __str__(self):
        return self.site_name
