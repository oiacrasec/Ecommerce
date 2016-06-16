from django.conf.urls import url
from payment.views import PaymentProcessView, PaymentDoneView, PaymentCanceledView

urlpatterns = [
    url(r'^process/$', PaymentProcessView.as_view(), name='process'),
    url(r'^done/$', PaymentDoneView.as_view(), name='done'),
    url(r'^canceled/$', PaymentCanceledView.as_view(), name='canceled'),
]
