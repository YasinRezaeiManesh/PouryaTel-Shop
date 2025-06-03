from datetime import time
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from product_module.models import Product
from .models import OrderDetail, Order
from django.conf import settings
import requests
import json


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
                    new_detail = OrderDetail(product_id=product_id, count=count, order_id=current_order.id,
                                             color=product_color)
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


MERCHANT = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
ZP_API_REQUEST = "https://api.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify/'


# class OrderPayView(View):
#     def get(self, request):
#         data = {
#             'MerchantID': settings.MERCHANT,
#             'Amount': amount,
#             'Description': description,
#             'CallbackURL': CallbackURL,
#         }
#         data = json.dumps(data)
#         headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#         res = requests.post(ZP_API_REQUEST, data=data, headers=headers)
#
#         if res.status_code == 200:
#             response = res.json()
#             if response['Status'] == 100:
#                 url = f"{ZP_API_STARTPAY}{response['Authority']}"
#                 return redirect(url)
#         else:
#             return HttpResponse(str(res.json()['errors']))
#
#
# class VerifyPayView(View):
#     def get(self, request):
#         authority = request.GET.get('Authority')
#         data = {
#             'MerchantID': settings.MERCHANT,
#             'Amount': amount,
#             'Authority': authority,
#         }
#         data = json.dumps(data)
#         headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#         res = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#         if res.status_code == 200:
#             response = res.json()
#             if response['Status'] == 100:
#                 return HttpResponse({'Status': response['Status'], 'RefID': response['RefID']})
#             else:
#                 HttpResponse({'Status': response['Status'], 'RefID': response['RefID']})
#         return HttpResponse('پرداخت ناموفق')

# def send_request(request):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Description": description,
#         "Phone": phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#
#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
#                         'authority': response['Authority']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response
#
#     except requests.exceptions.Timeout:
#         return {'status': False, 'code': 'timeout'}
#     except requests.exceptions.ConnectionError:
#         return {'status': False, 'code': 'connection error'}
#
#
# def verify(authority):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#
#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             return {'status': True, 'RefID': response['RefID']}
#         else:
#             return {'status': False, 'code': str(response['Status'])}
#     return response

@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))
    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
    }
    req_header = {"accept": "application/json", "content-type": "application/json"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error message: {e_message}")


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority,
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()
                ref_str = req.json()['data']['message']
                return render(request, 'order_module/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
                })
            elif t_status == 101:
                return render(request, 'order_module/payment_result.html', {
                    'info': 'این تراکنش قبلا ثبت شده است'
                })
            else:
                return render(request, 'order_module/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return render(request, 'order_module/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'order_module/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })
