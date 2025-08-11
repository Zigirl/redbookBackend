from django.urls import path, include

from orders.views import order_create, order_list, order_detail, order_update, order_delete

urlpatterns = [

    path('order_create', order_create),
    path('order_list', order_list),
    path('order_detail', order_detail),
    path('order_update', order_update),
    path('order_delete', order_delete)

]