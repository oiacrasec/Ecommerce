from django.conf.urls import url
from shop.views import ProductListView, ProductDetailView

urlpatterns = [
    # url(r'^list-user/$', UserList.as_view(), name='list-user'),
    # url(r'^edit-group/(?P<id>\d+)/$', GroupEdit.as_view(), name='edit-group'),
    # url(r'^create-group/$', GroupCreate.as_view(), name='create-group'),

    url(r'^list-product/$', ProductListView.as_view(), name='product_list'),
    url(r'^list-product/(?P<category_slug>[-\w]+)/$', ProductListView.as_view(), name='product_list_by_category'),
    url(r'^detail-product/(?P<id>\d+)/(?P<slug>[-\w]+)/$', ProductDetailView.as_view(), name='product_detail'),
]
