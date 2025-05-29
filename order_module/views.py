from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from .models import *
from product_module.models import Product


# Create your views here.


def add_to_order(request: HttpRequest):
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))
    product_color = request.GET.get('color')
    if count < 1:
        return JsonResponse({
            'status': 'invalid count',
            'text': 'مقدار وارد شده نامعبتر میباشد',
            'title': 'خطا',
            'icon': 'error',
            'confirm_button_text': 'باشه ، ممنون',
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, inventory=True).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if not current_order.is_close:
                if current_order_detail is not None:
                    current_order_detail.count += count
                    current_order_detail.save()
                    return JsonResponse({
                        'status': 'success',
                        'text': 'محصول مورد نظر با موفقیت به سبد خرید شما افزوده شد',
                        'title': 'عملیات موفقیت آمیز بود',
                        'icon': 'success',
                        'confirm_button_text': 'باشه ، ممنون',
                    })
                else:
                    new_detail = OrderDetail(product_id=product_id, count=count, order_id=current_order.id, color=product_color)
                    new_detail.save()
                    return JsonResponse({
                        'status': 'success',
                        'text': 'محصول مورد نظر با موفقیت به سبد خرید شما افزوده شد',
                        'title': 'عملیات موفقیت آمیز بود',
                        'icon': 'success',
                        'confirm_button_text': 'باشه ، ممنون',
                    })
            else:
                return JsonResponse({
                    'status': 'card close',
                    'text': 'کاربر گرامی سبد خرید شما بسته میباشد ، لطفا در ابتدا سبد خرید خود را کامل کنید',
                    'title': 'سبد خرید شما بسته میباشد',
                    'icon': 'error',
                    'confirm_button_text': 'باشه ، ممنون',
                })
        else:
            return JsonResponse({
                'status': 'not found',
                'text': 'محصول مورد نظر پیدا نشد',
                'title': 'خطا',
                'icon': 'error',
                'confirm_button_text': 'باشه ، ممنون',
            })
    else:
        return JsonResponse({
            'status': 'user is not authenticated',
            'text': 'لطفا در ابتدا وارد حساب کاربری خود در وبسایت شوید',
            'title': 'خطا',
            'icon': 'error',
            'confirm_button_text': 'ورود به حساب کاربری',
        })



