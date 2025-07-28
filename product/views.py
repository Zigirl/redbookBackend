from django.http import JsonResponse


# 添加用户
def product_add(request):
    return JsonResponse({'status': 'ok'})


# 删除用户
def product_delete(request):
    return JsonResponse({'status': 'ok'})


# 修改用户
def product_update(request):
    return JsonResponse({'status': 'ok'})


# 查询用户
def product_list(request):
    return JsonResponse({'status': 'ok'})
