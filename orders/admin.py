from django.contrib import admin
from .models import Cart, CartObject, Order, BillingInfo, PaymentType

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CartObject)
admin.site.register(BillingInfo)
admin.site.register(PaymentType)