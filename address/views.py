from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import UserAddress


@csrf_exempt
@require_http_methods(["POST"])
def get_user_addresses(request):
    """获取用户地址列表"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': '用户ID不能为空'})
        
        addresses = UserAddress.objects.filter(userId=user_id)
        address_list = []
        
        for address in addresses:
            address_list.append({
                'address_id': address.address_id,
                'userId': address.userId,
                'recipient': address.recipient,
                'phone': address.phone,
                'country_code': address.country_code,
                'province': address.province,
                'city': address.city,
                'district': address.district,
                'street': address.street,
                'postal_code': address.postal_code,
                'full_address': address.get_full_address(),
                'formatted_address': address.get_formatted_address(),
                'address_tag': address.address_tag,
                'address_tag_display': address.get_address_tag_display(),
                'is_default': address.is_default,
                'created_at': address.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'success': True,
            'data': address_list,
            'message': '获取地址列表成功'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'获取地址列表失败: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def add_user_address(request):
    """新增用户地址"""
    try:
        data = json.loads(request.body)
        user_id = data.get('userId')
        recipient = data.get('recipient')
        phone = data.get('phone')
        country_code = data.get('country_code', 'CN')
        province = data.get('province')
        city = data.get('city')
        district = data.get('district')
        street = data.get('street')
        postal_code = data.get('postal_code')
        address_tag = data.get('address_tag', '家')
        is_default = data.get('is_default', False)
        
        # 验证必填字段
        required_fields = ['userId', 'recipient', 'phone', 'province', 'city', 'district', 'street']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'{field} 不能为空'
                })
        
        # 如果设置为默认地址，先取消其他默认地址
        if is_default:
            UserAddress.objects.filter(userId=user_id, is_default=True).update(is_default=False)
        
        # 创建新地址
        new_address = UserAddress.objects.create(
            userId=user_id,
            recipient=recipient,
            phone=phone,
            country_code=country_code,
            province=province,
            city=city,
            district=district,
            street=street,
            postal_code=postal_code,
            address_tag=address_tag,
            is_default=is_default
        )
        
        return JsonResponse({
            'success': True,
            'data': {
                'address_id': new_address.address_id,
                'userId': new_address.userId,
                'recipient': new_address.recipient,
                'phone': new_address.phone,
                'country_code': new_address.country_code,
                'province': new_address.province,
                'city': new_address.city,
                'district': new_address.district,
                'street': new_address.street,
                'postal_code': new_address.postal_code,
                'full_address': new_address.get_full_address(),
                'formatted_address': new_address.get_formatted_address(),
                'address_tag': new_address.address_tag,
                'address_tag_display': new_address.get_address_tag_display(),
                'is_default': new_address.is_default,
                'created_at': new_address.created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            'message': '新增地址成功'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'新增地址失败: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def set_default_address(request):
    """设置默认地址"""
    try:
        data = json.loads(request.body)
        user_id = data.get('userId')
        address_id = data.get('address_id')
        
        if not all([user_id, address_id]):
            return JsonResponse({
                'success': False,
                'message': '参数不完整'
            })
        
        # 先取消该用户的所有默认地址
        UserAddress.objects.filter(userId=user_id, is_default=True).update(is_default=False)
        
        # 设置新的默认地址
        address = UserAddress.objects.get(address_id=address_id, userId=user_id)
        address.is_default = True
        address.save()
        
        return JsonResponse({
            'success': True,
            'message': '设置默认地址成功'
        })
    
    except UserAddress.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '地址不存在'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'设置默认地址失败: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user_address(request, address_id):
    """删除用户地址"""
    try:
        data = json.loads(request.body)
        user_id = data.get('userId')
        
        if not user_id:
            return JsonResponse({
                'success': False,
                'message': '用户ID不能为空'
            })
        
        address = UserAddress.objects.get(address_id=address_id, userId=user_id)
        address.delete()
        
        return JsonResponse({
            'success': True,
            'message': '删除地址成功'
        })
    
    except UserAddress.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '地址不存在'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除地址失败: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["GET"])
def search_address(request):
    """搜索地址（可以集成地图API）"""
    try:
        keyword = request.GET.get('keyword', '')
        if not keyword:
            return JsonResponse({
                'success': False,
                'message': '搜索关键词不能为空'
            })
        
        # 这里可以集成地图API进行地址搜索
        # 目前使用模拟数据
        mock_results = [
            f'{keyword}附近地址1',
            f'{keyword}附近地址2',
            f'{keyword}附近地址3'
        ]
        
        return JsonResponse({
            'success': True,
            'data': mock_results,
            'message': '搜索成功'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'搜索地址失败: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["GET"])
def get_provinces(request):
    """获取省份列表"""
    try:
        # 这里可以从数据库或配置文件获取省份列表
        provinces = [
            '北京市', '天津市', '河北省', '山西省', '内蒙古自治区',
            '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省',
            '浙江省', '安徽省', '福建省', '江西省', '山东省',
            '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区',
            '海南省', '重庆市', '四川省', '贵州省', '云南省',
            '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区',
            '新疆维吾尔自治区', '台湾省', '香港特别行政区', '澳门特别行政区'
        ]
        
        return JsonResponse({
            'success': True,
            'data': provinces,
            'message': '获取省份列表成功'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'获取省份列表失败: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["GET"])
def get_cities(request):
    """根据省份获取城市列表"""
    try:
        province = request.GET.get('province', '')
        if not province:
            return JsonResponse({
                'success': False,
                'message': '省份参数不能为空'
            })
        
        # 这里可以根据省份从数据库或配置文件获取城市列表
        # 目前使用模拟数据
        cities = [
            f'{province}城市1',
            f'{province}城市2',
            f'{province}城市3'
        ]
        
        return JsonResponse({
            'success': True,
            'data': cities,
            'message': '获取城市列表成功'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'获取城市列表失败: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["GET"])
def get_districts(request):
    """根据城市获取区县列表"""
    try:
        city = request.GET.get('city', '')
        if not city:
            return JsonResponse({
                'success': False,
                'message': '城市参数不能为空'
            })
        
        # 这里可以根据城市从数据库或配置文件获取区县列表
        # 目前使用模拟数据
        districts = [
            f'{city}区县1',
            f'{city}区县2',
            f'{city}区县3'
        ]
        
        return JsonResponse({
            'success': True,
            'data': districts,
            'message': '获取区县列表成功'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'获取区县列表失败: {str(e)}'
        })
