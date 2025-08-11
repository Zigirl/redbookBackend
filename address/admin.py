from django.contrib import admin
from .models import UserAddress


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['address_id', 'userId', 'recipient', 'phone', 'get_formatted_address', 'address_tag', 'is_default', 'created_at']
    list_filter = ['country_code', 'address_tag', 'is_default', 'created_at', 'province', 'city']
    search_fields = ['recipient', 'phone', 'province', 'city', 'district', 'street', 'userId']
    list_editable = ['is_default', 'address_tag']
    readonly_fields = ['created_at', 'updated_at', 'get_full_address']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('userId', 'recipient', 'phone', 'address_tag')
        }),
        ('地址信息', {
            'fields': ('country_code', 'province', 'city', 'district', 'street', 'postal_code')
        }),
        ('状态信息', {
            'fields': ('is_default', 'created_at', 'updated_at')
        }),
        ('完整地址', {
            'fields': ('get_full_address',),
            'classes': ('collapse',)
        }),
    )
    
    def get_formatted_address(self, obj):
        return obj.get_formatted_address()
    get_formatted_address.short_description = '地址'
    
    def get_full_address(self, obj):
        return obj.get_full_address()
    get_full_address.short_description = '完整地址'
