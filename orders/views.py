from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from django.http import JsonResponse


# 创建订单
@csrf_exempt
def order_create(request):
    if request.method == 'POST':
        try:
            # 解析JSON请求体
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': '无效的JSON格式'})
            
            # 获取订单数据
            user_id = data.get('user_id')
            total_amount = data.get('total_amount')
            pay_amount = data.get('pay_amount')
            address_id = data.get('address_id')
            payment_method = data.get('payment_method')
            remark = data.get('remark')
            
            # 验证必填字段
            if not all([user_id, total_amount, pay_amount, address_id]):
                return JsonResponse({'status': 'error', 'message': '缺少必填字段'})
            
            # 创建订单
            order = Order()
            order.user_id = user_id
            order.total_amount = total_amount
            order.pay_amount = pay_amount
            order.address_id = address_id
            order.payment_method = payment_method
            order.remark = remark
            order.order_status = 1  # 默认待支付状态
            
            order.save()
            
            return JsonResponse({
                'status': 'ok', 
                'message': '订单创建成功',
                'data': {
                    'order_id': order.order_id,
                    'order_no': order.order_no,
                    'order_status': order.order_status
                }
            })
        except Exception as e:
            print(f"创建订单失败: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})


# 查询订单列表
def order_list(request):
    if request.method == 'GET':
        try:
            # 获取查询参数
            user_id = request.GET.get('user_id')
            order_status = request.GET.get('order_status')
            
            # 构建查询条件
            orders = Order.objects.all()
            
            if user_id:
                orders = orders.filter(user_id=user_id)
            if order_status:
                orders = orders.filter(order_status=order_status)
            
            # 按创建时间倒序排列
            orders = orders.order_by('-created_at')
            
            # 转换为JSON格式
            order_list = []
            for order in orders:
                order_data = {
                    'order_id': order.order_id,
                    'order_no': order.order_no,
                    'user_id': order.user_id,
                    'order_status': order.order_status,
                    'total_amount': float(order.total_amount),
                    'pay_amount': float(order.pay_amount),
                    'payment_method': order.payment_method,
                    'address_id': order.address_id,
                    'remark': order.remark,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                order_list.append(order_data)
            
            return JsonResponse({'status': 'ok', 'data': order_list})
        except Exception as e:
            print(f"查询订单列表失败: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})


# 查询单个订单详情
@csrf_exempt
def order_detail(request):
    if request.method == 'POST':
        try:
            # 解析JSON请求体
            try:
                data = json.loads(request.body)
                order_id = data.get('order_id')
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': '无效的JSON格式'})
            
            if not order_id:
                return JsonResponse({'status': 'error', 'message': '缺少order_id参数'})
            
            # 查询指定的订单
            order = Order.objects.get(order_id=order_id)
            
            # 转换为JSON格式
            order_data = {
                'order_id': order.order_id,
                'order_no': order.order_no,
                'user_id': order.user_id,
                'order_status': order.order_status,
                'total_amount': float(order.total_amount),
                'pay_amount': float(order.pay_amount),
                'payment_method': order.payment_method,
                'address_id': order.address_id,
                'remark': order.remark,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return JsonResponse({'status': 'ok', 'data': order_data})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '订单不存在'})
        except Exception as e:
            print(f"查询订单详情失败: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})


# 更新订单状态
@csrf_exempt
def order_update(request):
    if request.method == 'POST':
        try:
            # 解析JSON请求体
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': '无效的JSON格式'})
            
            order_id = data.get('order_id')
            order_status = data.get('order_status')
            payment_method = data.get('payment_method')
            remark = data.get('remark')
            
            if not order_id:
                return JsonResponse({'status': 'error', 'message': '缺少order_id参数'})
            
            # 查询并更新订单
            order = Order.objects.get(order_id=order_id)
            
            if order_status is not None:
                order.order_status = order_status
            if payment_method is not None:
                order.payment_method = payment_method
            if remark is not None:
                order.remark = remark
            
            order.save()
            
            return JsonResponse({
                'status': 'ok', 
                'message': '订单更新成功',
                'data': {
                    'order_id': order.order_id,
                    'order_status': order.order_status
                }
            })
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '订单不存在'})
        except Exception as e:
            print(f"更新订单失败: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})


# 删除订单
@csrf_exempt
def order_delete(request):
    if request.method == 'POST':
        try:
            # 解析JSON请求体
            try:
                data = json.loads(request.body)
                order_id = data.get('order_id')
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': '无效的JSON格式'})
            
            if not order_id:
                return JsonResponse({'status': 'error', 'message': '缺少order_id参数'})
            
            # 查询并删除订单
            order = Order.objects.get(order_id=order_id)
            order.delete()
            
            return JsonResponse({'status': 'ok', 'message': '订单删除成功'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '订单不存在'})
        except Exception as e:
            print(f"删除订单失败: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '不支持的请求方法'})
