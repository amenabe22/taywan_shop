from django.contrib import admin
from .models import Cart, CartObject, Order, BillingInfo, PaymentType, PaymentDetail


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'billing_info', 'ordered_by',
                    'order_status', 'paid_already', 'payment_type', 'reference_no',)
    list_editable = ('order_status', 'payment_type', 'reference_no',)
    list_display_links = ('order_id',)
    search_fields = ('order_id',)


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'core_transaction_outlet',
                    'payment_detail', 'available',)


admin.site.register(Cart)
admin.site.register(CartObject)
admin.site.register(BillingInfo)
admin.site.register(PaymentDetail)
admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
