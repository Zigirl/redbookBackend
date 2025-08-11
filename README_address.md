# 地址管理系统使用说明
### 启动
docker build -t redbook-backend .

docker run -d   --name redbook-app   -p 8000:8000   -v $(pwd)/media:/app/media   -v $(pwd)/logs:/app/logs   redbook-backend
## 概述

这是一个完整的地址管理系统，包含后端API和前端界面，支持用户地址的增删改查、默认地址设置、四级行政区划选择等功能。

## 功能特性

### 1. 地址管理
- ✅ 新增收货地址
- ✅ 查看地址列表
- ✅ 编辑地址信息
- ✅ 删除地址
- ✅ 设置默认地址

### 2. 地址字段
- **基本信息**: 收件人姓名、联系电话、地址标签
- **四级行政区划**: 国家代码、省份、城市、区县、街道地址
- **其他信息**: 邮政编码、是否默认地址、创建/更新时间

### 3. 地址标签
- 家
- 公司
- 学校
- 其他

### 4. 支持的国家/地区
- 中国 (CN)
- 美国 (US)
- 日本 (JP)
- 韩国 (KR)
- 英国 (GB)
- 德国 (DE)
- 法国 (FR)

## 技术架构

### 后端 (Django)
- **模型**: `address/models.py` - 定义地址数据结构
- **视图**: `address/views.py` - 提供RESTful API接口
- **URL**: `address/urls.py` - 路由配置
- **Admin**: `address/admin.py` - 后台管理界面

### 前端 (HTML + JavaScript)
- **地址选择页面**: `templates/address_selection.html`
- **产品详情页面**: `templates/product_detail.html`
- **样式**: Bootstrap 5 + 自定义CSS
- **交互**: 原生JavaScript + Fetch API

## API接口说明

### 1. 获取用户地址列表
```
GET /address/api/addresses/?user_id={user_id}
```

### 2. 新增地址
```
POST /address/api/addresses/add/
Content-Type: application/json

{
    "userId": 1,
    "recipient": "张三",
    "phone": "13800138000",
    "country_code": "CN",
    "province": "北京市",
    "city": "北京市",
    "district": "朝阳区",
    "street": "建国路88号",
    "postal_code": "100000",
    "address_tag": "家",
    "is_default": false
}
```

### 3. 设置默认地址
```
POST /address/api/addresses/set-default/
Content-Type: application/json

{
    "userId": 1,
    "address_id": 1
}
```

### 4. 删除地址
```
DELETE /address/api/addresses/{address_id}/
Content-Type: application/json

{
    "userId": 1
}
```

### 5. 获取地区数据
```
GET /address/api/provinces/          # 获取省份列表
GET /address/api/cities/?province={province}     # 获取城市列表
GET /address/api/districts/?city={city}          # 获取区县列表
```

## 使用方法

### 1. 在产品页面集成
```html
<!-- 参与订单按钮 -->
<button class="btn btn-primary" onclick="showAddressSelection()">
    参与订单
</button>

<!-- 地址选择模态框 -->
<div id="addressModal" class="modal">
    <iframe id="addressFrame" src="/templates/address_selection.html"></iframe>
</div>

<script>
function showAddressSelection() {
    const modal = document.getElementById('addressModal');
    const iframe = document.getElementById('addressFrame');
    iframe.src = `/templates/address_selection.html?user_id=${currentUserId}`;
    modal.style.display = 'block';
}

// 地址选择回调
function onAddressSelected(address) {
    console.log('选中的地址:', address);
    // 处理地址选择后的逻辑
}
</script>
```

### 2. 独立使用地址选择页面
```html
<iframe src="/templates/address_selection.html?user_id=1" 
        width="100%" height="600px" frameborder="0">
</iframe>
```

## 数据库迁移

### 1. 创建迁移文件
```bash
python manage.py makemigrations address
```

### 2. 应用迁移
```bash
python manage.py migrate
```

### 3. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

## 配置说明

### 1. 添加到Django项目
在 `settings.py` 中添加：
```python
INSTALLED_APPS = [
    # ... 其他应用
    "address.apps.AddressConfig",
]
```

### 2. 配置URL路由
在 `urls.py` 中添加：
```python
urlpatterns = [
    # ... 其他URL
    path('address/', include('address.urls')),
]
```

## 自定义配置

### 1. 添加更多国家/地区
在 `address/models.py` 中的 `COUNTRY_CHOICES` 添加新的选项。

### 2. 添加更多地址标签
在 `address/models.py` 中的 `ADDRESS_TAG_CHOICES` 添加新的标签。

### 3. 集成真实地图API
在 `address/views.py` 中的 `search_address` 函数中集成真实的地图搜索API。

### 4. 地区数据源
可以替换 `get_provinces`、`get_cities`、`get_districts` 函数中的模拟数据，使用真实的地区数据库。

## 注意事项

1. **用户认证**: 当前版本使用简单的用户ID参数，建议集成Django的认证系统
2. **数据验证**: 前端和后端都有基本的数据验证，但可以根据需要增强
3. **安全性**: 生产环境中建议添加CSRF保护、权限验证等安全措施
4. **性能**: 对于大量地址数据，建议添加分页和搜索功能

## 扩展功能建议

1. **地址搜索**: 集成地图API，支持地址搜索和自动补全
2. **地址验证**: 添加地址有效性验证
3. **批量操作**: 支持批量删除、批量设置默认地址
4. **地址导入**: 支持从Excel、CSV等格式批量导入地址
5.