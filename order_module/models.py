from django.db import models

from account_module.models import User
from product_module.models import Product


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    is_close = models.BooleanField(default=False, verbose_name='بسته شده')
    date_paid = models.DateField(verbose_name='تاریخ پرداخت', blank=True, null=True)
    post_paid = models.IntegerField(verbose_name='هزینه پستی', default=50000)

    def post_price(self):
        post_price = 0
        post_price += self.post_paid
        return post_price

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                if order_detail.product.off:
                    total_amount += order_detail.product.off_price * order_detail.count
                else:
                    total_amount += order_detail.product.price * order_detail.count
        if total_amount > 0:
            total_amount += self.post_paid

        return total_amount

    class Meta:
        verbose_name = 'سبد'
        verbose_name_plural = 'سبد های خرید'

    def __str__(self):
        return str(self.user)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(verbose_name='قیمت نهایی تکی محصول', null=True, blank=True)
    count = models.IntegerField(verbose_name='تعداد')
    color = models.CharField(max_length=100, verbose_name='رنگ کالا', default='دلخواه')

    def get_total_price(self):
        if self.product.off:
            return self.count * self.product.off_price
        else:
            return self.count * self.product.price

    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'جزییات سبد خرید'

    def __str__(self):
        return str(self.order)
