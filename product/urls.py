from django.urls import path, include

from product.views import product_add, product_delete, product_update, product_list, product_upload, product_detail

urlpatterns = [

    path('product_add', product_add),
    path('product_delete', product_delete),
    path('product_update', product_update),
    path('product_list', product_list),
    path('product_upload', product_upload),
    path('product_detail', product_detail)

]