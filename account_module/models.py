from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to="images/user_avatar", verbose_name='تصویر پروفایل', blank=True, null=True)
    email_active_code = models.CharField(verbose_name='کد فعالسازی ایمیل', unique=True, max_length=200)
    number = models.CharField(verbose_name='شماره تماس', unique=True, max_length=11)
    about_user = models.TextField(verbose_name='درباره شخص', default='')
    address = models.TextField(verbose_name='آدرس شخص', default='')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.get_full_name()
