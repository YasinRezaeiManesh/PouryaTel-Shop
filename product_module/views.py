from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


# Create your views here.


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product_module/product_list.html'
    paginate_by = 12

    def get_queryset(self):
        query = super().get_queryset()
        sub_cat = self.kwargs.get('url_cat')
        mobile_company = self.kwargs.get('url_mobile_company')
        attachment = self.kwargs.get('url_attachment')
        if sub_cat:
            query = query.filter(sub_cat__url_title__iexact=sub_cat)
        elif mobile_company:
            query = query.filter(mobile_company__url_address__iexact=mobile_company)
        elif attachment:
            query = query.filter(attachment__url_address__iexact=attachment)
        return query

    def get_context_data(self, **kwargs):
        context = {
            self.context_object_name: self.get_queryset(),
            'mobile_companies': MobileCompany.objects.filter(is_active=True),
            'attachments': Attachments.objects.all(),
            'categories': ProductCategories.objects.all(),
        }

        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_module/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        loaded_product = self.object
        context['comments'] = ProductComments.objects.filter(product_id=loaded_product.id, success=True).order_by('-date')
        context['comments_count'] = ProductComments.objects.filter(product_id=loaded_product.id).count()
        context['product_gallery'] = ProductGallery.objects.filter(product_id=loaded_product.id).all()
        context['related_products'] = Product.objects.filter(sub_cat_id=loaded_product.sub_cat.id).exclude(id=loaded_product.id)
        return context


def search(request):
    if request.method == 'POST':
        query_name = request.POST.get('search_input')
        if query_name:
            result = Product.objects.filter(title__icontains=query_name)
            if result:
                context = {
                    'products': result,
                    'mobile_companies': MobileCompany.objects.filter(is_active=True),
                    'attachments': Attachments.objects.all(),
                    'categories': ProductCategories.objects.all(),
                }
                return render(request, 'product_module/product_list.html', context)

            return render(request, 'product_module/product_not_found.html')


def send_product_comment(request):
    if request.user.is_authenticated:
        product_comment = request.GET.get('productComment')
        product_parent = request.GET.get('parentId')
        product_id = request.GET.get('productId')
        new_comment = ProductComments(product_id=product_id, comment=product_comment, parent_id=product_parent,
                                      user_id=request.user.id)
        new_comment.save()
        return HttpResponse('success')
