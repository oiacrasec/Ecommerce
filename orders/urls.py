from django.conf.urls import url
from orders.views import OrderCreateView, AdminOrderDetailView, AdminOrderPDFView

urlpatterns = [
    url(r'^create/$', OrderCreateView.as_view(), name='order_create'),

    url(r'^admin/order/(?P<order_id>\d+)/$', AdminOrderDetailView.as_view(), name='admin_order_detail'),

    url(r'^admin/order/(?P<order_id>\d+)/pdf/$', AdminOrderPDFView.as_view(), name='admin_order_pdf'),
]
