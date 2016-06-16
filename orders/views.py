import os
from cart.cart import Cart
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order
from orders.tasks import order_created
import weasyprint


class OrderCreateView(CreateView):
    template_name = 'orders/order/create.html'
    form_class = OrderCreateForm
    order = None

    def form_valid(self, form):
        self.order = form.save()
        cart = Cart(self.request)
        for item in cart:
            OrderItem.objects.create(order=self.order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()

        # launch asynchronous task, only work if worker is running
        order_created.delay(self.order.id)  # set the order in the session

        # return render(self.request, 'orders/order/created.html', {'order': self.order})

        # redirect to the payment (paypal)
        self.request.session['order_id'] = self.order.id
        return redirect(reverse('payment:process'))


class AdminOrderDetailView(TemplateView):
    template_name = 'admin/orders/order/detail.html'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminOrderDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminOrderDetailView, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=context['order_id'])
        return context


class AdminOrderPDFView(TemplateView):

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        html = render_to_string('orders/order/pdf.html', {'order': order})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.id)

        css_path = os.path.join(settings.STATICFILES_DIRS[0], 'css/pdf.css')
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(css_path)])
        return response
