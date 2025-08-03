from django.http import JsonResponse
from django.shortcuts import render

from user.models import UserInfo


# 登录界面
def index(request):
    return render(request, 'login.html')

# 用户登录
def login(request):
    print(request.POST.get('account'))
    print(request.POST.get('password'))
    if UserInfo.objects.filter(account=request.POST.get('account'),password=request.POST.get('password')).exists():
        user = UserInfo.objects.filter(account=request.POST.get('account'), password=request.POST.get('password'))[0]
        # 添加session信息
        request.session['userId'] = user.userId
        request.session['account'] = user.account
        request.session['password'] = user.password
        request.session['username'] = user.username
        request.session['isManager'] = user.isManager
        return render(request, 'index.html')
    else:
        return render(request, 'login.html', {'error': "账号或密码错误"})

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
