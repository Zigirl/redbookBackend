from django.urls import path, include

from user.views import user_add, user_delete, user_update, user_list

urlpatterns = [

    path('user_add', user_add),
    path('user_delete', user_delete),
    path('user_update', user_update),
    path('user_list',user_list)

]
