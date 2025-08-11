from django.db import models
from django.utils import timezone
import uuid

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (1, '待支付'),
        (2, '已支付'),
        (3, '已发货'),
        (4, '已完成'),
        (5, '已取消'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('alipay', '支付宝'),
        ('wechatpay', '微信支付'),
        ('creditcard', '信用卡'),
    ]
    
    order_id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    order_no = models.CharField(max_length=32, unique=True)
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    address_id = models.BigIntegerField()
    remark = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = '订单'
    
    def save(self, *args, **kwargs):
        if not self.order_no:
            # 生成订单编号：时间戳 + 随机字符串
            self.order_no = f"{int(timezone.now().timestamp())}{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)