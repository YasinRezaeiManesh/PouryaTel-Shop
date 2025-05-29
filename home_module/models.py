from django.db import models

# Create your models here.


class HomeSlider(models.Model):
    image = models.ImageField(upload_to='images/home_sliders', verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'اسلایدر تصاویر خانه'
