from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import *
from account_module.models import User
from django.views import View
from django.contrib.auth import logout
from order_module.models import *


# Create your views here.


class UserPanelView(TemplateView):
    template_name = 'user_panel_module/panel.html'


class EditPanelView(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditPanelForm(instance=current_user)
        context = {
            'form': edit_form,
            'user': current_user,
        }
        return render(request, 'user_panel_module/edit_panel.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditPanelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        context = {
            'form': edit_form,
            'user': current_user,
        }
        return render(request, 'user_panel_module/edit_panel.html', context)


class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        form = ChangePasswordForm()
        context = {
            'form': form,
        }
        return render(request, 'user_panel_module/change_password.html', context)

    def post(self, request: HttpRequest):
        user: User = User.objects.filter(id=request.user.id).first()
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            if user.check_password(current_password):
                new_password = form.cleaned_data.get('new_password')
                user.set_password(new_password)
                user.save()
                logout(request)
                return redirect(reverse('login'))
            else:
                form.add_error('current_password', 'رمز عبور فعلی اشتباه میباشد')
        context = {
            'form': form,
        }
        return render(request, 'user_panel_module/change_password.html', context)


class UserOrder(TemplateView):
    template_name = 'user_panel_module/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                 user_id=self.request.user.id)
        context['order'] = current_order
        context['post_price'] = current_order.post_price()
        context['total_amount'] = current_order.calculate_total_price()
        return context


def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None:
        return JsonResponse({
            'status': 'not found detail or state'
        })
    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'not found detail'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state invalid'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    context = {
        'order': current_order,
        'total_amount': total_amount,
        'post_price': current_order.post_price()
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/order_content.html', context)
    })


def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'success': "detail_not_found_id",
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__is_close=False,
                                                             order__user_id=request.user.id).delete()
    if deleted_count:
        return JsonResponse({
            'success': "detail_not_found",
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'total_amount': total_amount,
        'post_price': current_order.post_price()
    }
    return JsonResponse({
        'status': "success",
        'body': render_to_string('user_panel_module/order_content.html', context)
    })


def panel_menu(request):
    return render(request, 'user_panel_module/panel_menu.html')
