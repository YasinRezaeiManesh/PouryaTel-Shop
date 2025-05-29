from django.urls import path
from .views import *


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('mob-comp/<str:url_mobile_company>', ProductListView.as_view(), name='mobile_company'),
    path('attachment/<str:url_attachment>', ProductListView.as_view(), name='attachment'),
    path('cat/<str:url_cat>', ProductListView.as_view(), name='product_cat'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('search/', search, name='search'),
    path('product-comment/', send_product_comment, name='product_comment'),
]
