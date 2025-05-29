from django.urls import path
from .views import *

urlpatterns = [
    path('', UserPanelView.as_view(), name='user_panel'),
    path('edit/', EditPanelView.as_view(), name='edit_panel'),
    path('change-pass/', ChangePasswordView.as_view(), name='change_pass'),
    path('order/', UserOrder.as_view(), name='order'),
    path('change-order-detail-count', change_order_detail_count, name='change_order_detail_count'),
    path('remove-order-detail/', remove_order_detail, name='remove_order_detail'),

]
