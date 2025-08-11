from django.urls import path
from . import views

app_name = 'address'

urlpatterns = [
    # 地址相关API
    path('addresses_list/', views.get_user_addresses, name='get_user_addresses'),
    path('add/', views.add_user_address, name='add_user_address'),
    path('api/addresses/set-default/', views.set_default_address, name='set_default_address'),
    path('api/addresses/<int:address_id>/delete/', views.delete_user_address, name='delete_user_address'),
    path('api/addresses/search/', views.search_address, name='search_address'),
    
    # 地区选择API
    path('api/provinces/', views.get_provinces, name='get_provinces'),
    path('api/cities/', views.get_cities, name='get_cities'),
    path('api/districts/', views.get_districts, name='get_districts'),
]
