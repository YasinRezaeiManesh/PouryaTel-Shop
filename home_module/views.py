from django.shortcuts import render
from django.views.generic import TemplateView
from order_module.models import Order
from about_module.models import Contact, Info
from .models import *
from product_module.models import *
from django.db.models import Count, Sum


# Create your views here.


class HomeView(TemplateView):
    template_name = 'home_module/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.objects.order_by('-id')[:10]
        context['off_products'] = Product.objects.filter(inventory=True, off=True)[:10]
        context['mobiles'] = Product.objects.filter(inventory=True, is_mobile=True)
        context['slider_pic'] = HomeSlider.objects.all()
        context['categories'] = ProductCategories.objects.all()
        most_bought_product = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:8]
        context['most_bought_product'] = most_bought_product
        return context


def site_header_component(request):
    context = {
        'info': Info.objects.all().first(),
        'mobile_companies': MobileCompany.objects.all(),
        'attachments': Attachments.objects.all(),
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    context = {
        'contact': Contact.objects.all().first(),
        'info': Info.objects.all().first(),
        'order': current_order,
        'total_amount': current_order.calculate_total_price()
    }
    return render(request, 'shared/site_footer_component.html', context)
