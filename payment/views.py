from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order


class PaymentProcessView(TemplateView):
    template_name = 'payment/process.html'

    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
            'item_name': 'Order {}'.format(order.id),
            'invoice': str(order.id),
            'currency_code': 'BRL',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'payment/process.html', {'order': order, 'form': form})


class PaymentDoneView(TemplateView):
    template_name = 'payment/done.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentDoneView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return super(PaymentDoneView, self).render_to_response(context)


class PaymentCanceledView(TemplateView):
    template_name = 'payment/canceled.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentCanceledView, self).dispatch(request, *args, **kwargs)
