from django.db import models


class UserAddress(models.Model):
    """用户地址表"""
    COUNTRY_CHOICES = [
        ('CN', '中国'),
        ('US', '美国'),
        ('JP', '日本'),
        ('KR', '韩国'),
        ('GB', '英国'),
        ('DE', '德国'),
        ('FR', '法国'),
    ]
    
    ADDRESS_TAG_CHOICES = [
        ('家', '家'),
        ('公司', '公司'),
        ('学校', '学校'),
        ('其他', '其他'),
    ]
    
    address_id = models.AutoField(primary_key=True, verbose_name='地址ID')
    userId = models.IntegerField(verbose_name='用户ID（关联用户表）')
    recipient = models.CharField(max_length=50, verbose_name='收件人姓名')
    phone = models.CharField(max_length=20, verbose_name='收件人电话')
    
    # 四级行政区划
    country_code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='CN', verbose_name='国家代码')
    province = models.CharField(max_length=50, verbose_name='省份')
    city = models.CharField(max_length=50, verbose_name='城市')
    district = models.CharField(max_length=50, verbose_name='区县')
    street = models.CharField(max_length=200, verbose_name='街道地址')
    
    # 地址详情
    postal_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='邮政编码')
    
    # 地址标签和状态
    address_tag = models.CharField(max_length=20, choices=ADDRESS_TAG_CHOICES, default='家', verbose_name='地址标签')
    is_default = models.BooleanField(default=False, verbose_name='是否默认地址')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_addresses'
        verbose_name = '用户地址'
        verbose_name_plural = '用户地址'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.recipient} - {self.get_full_address()}"
    
    def get_full_address(self):
        """获取完整地址"""
        return f"{self.country_code} {self.province} {self.city} {self.district} {self.street}"
    
    def get_formatted_address(self):
        """获取格式化的地址（用于显示）"""
        return f"{self.province} {self.city} {self.district} {self.street}"
