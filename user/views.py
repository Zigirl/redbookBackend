from django.http import JsonResponse
from django.shortcuts import render


# 添加用户
def user_add(request):
    return JsonResponse({'status': 'ok'})


# 删除用户
def user_delete(request):
    return JsonResponse({'status': 'ok'})


# 修改用户
def user_update(request):
    return JsonResponse({'status': 'ok'})


# 查询用户
def user_list(request):
    return JsonResponse({'status': 'ok'})
