from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from user.models import UserInfo
from django.utils import timezone
import datetime
import json
from django.http import JsonResponse


# 产品上传
@csrf_exempt
def product_upload(request):
    if request.method == 'POST':
        try:
            # 获取表单数据
            account = request.POST.get('userAccount')
            project_title = request.POST.get('projectTitle')
            project_desc = request.POST.get('projectDesc')
            target_count = request.POST.get('targetCount')
            # 从前端获取时间，前端表单中时间字段id是timepicker
            target_time = request.POST.get('endTime')  # 调整为前端实际使用的字段名

            # 处理文件上传
            product_avatar = request.FILES.get('productAvatar')

            # 创建产品对象
            product = Product()
            # 根据账号查询用户ID
            try:
                user = UserInfo.objects.get(account=account)
                product.userId = user.userId
            except UserInfo.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '用户不存在'})
            product.projectTitle = project_title
            product.projectDesc = project_desc
            product.targetCount = int(target_count)
            product.currentCount = 0
            product.startTime = timezone.now()
            print(product)
            # 将字符串转换为datetime对象（只包含日期）
            # 确保target_time不为空且格式正确
            if not target_time:
                return JsonResponse({'status': 'error', 'message': '请选择目标时间'})
            try:
                product.endTime = datetime.datetime.strptime(target_time, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({'status': 'error', 'message': '时间格式不正确，请使用YYYY-MM-DD格式'})
            product.status = 0
            product.progress = 0

            # 保存图片
            if product_avatar:
                product.image = product_avatar

            product.save()
            print(f"产品保存成功: {product.groupId}")
            return JsonResponse({'status': 'ok', 'message': '上传成功', 'product_id': product.groupId})
        except Exception as e:
            print(f"产品保存失败: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})


# 添加用户
def product_add(request):
    return JsonResponse({'status': 'ok'})


# 删除商品
def product_delete(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('productId')
            if not product_id:
                return JsonResponse({'status': 'error', 'message': '缺少商品ID'})

            # 查询商品
            product = Product.objects.get(groupId=product_id)
            # 删除商品
            product.delete()
            return JsonResponse({'status': 'ok', 'message': '删除成功'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '商品不存在'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})


# 修改用户
def product_update(request):
    return JsonResponse({'status': 'ok'})


# 查询所有商品
def product_list(request):
    if request.method == 'GET':
        try:
            # 获取所有商品
            products = Product.objects.all()
            # 将商品数据转换为JSON格式
            product_list = []
            for product in products:
                product_data = {
                    'groupId': product.groupId,
                    'projectTitle': product.projectTitle,
                    'projectDesc': product.projectDesc,
                    'targetCount': product.targetCount,
                    'currentCount': product.currentCount,
                    'startTime': product.startTime.strftime('%Y-%m-%d %H:%M:%S'),
                    'endTime': product.endTime.strftime('%Y-%m-%d'),
                    'status': product.status,
                    'progress': product.progress,
                    'image': product.image.url if product.image else None
                }
                product_list.append(product_data)
            return JsonResponse({'status': 'ok', 'data': product_list})
        except Exception as e:
            print(f"查询商品失败: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})


# 根据groupId查询单个产品
@csrf_exempt
def product_detail(request):
    if request.method == 'POST':
        try:
            # 解析JSON请求体
            try:
                data = json.loads(request.body)
                group_id = data.get('groupId')
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': '无效的JSON格式'})
            
            if not group_id:
                return JsonResponse({'status': 'error', 'message': '缺少groupId参数'})
            
            # 查询指定的产品
            product = Product.objects.get(groupId=group_id)
            
            # 将产品数据转换为JSON格式
            product_data = {
                'groupId': product.groupId,
                'userId': product.userId,
                'projectTitle': product.projectTitle,
                'projectDesc': product.projectDesc,
                'targetCount': product.targetCount,
                'currentCount': product.currentCount,
                'startTime': product.startTime.strftime('%Y-%m-%d %H:%M:%S'),
                'endTime': product.endTime.strftime('%Y-%m-%d'),
                'status': product.status,
                'progress': product.progress,
                'image': product.image.url if product.image else None
            }
            
            return JsonResponse({'status': 'ok', 'data': product_data})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '产品不存在'})
        except Exception as e:
            print(f"查询产品详情失败: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})
