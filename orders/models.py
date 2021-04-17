import random
from uuid import uuid4
from django.db import models
from products.models import Product
from accounts.models import CustomUser


class CartObject(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    anon_usr = models.CharField(max_length=300, null=True, unique=True)
    anonnymous = models.BooleanField(default=True)
    items = models.ManyToManyField(CartObject, blank=True)

    def __str__(self):
        return str(self.cart_id)


class BillingInfo(models.Model):
    binfo_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)

    full_name = models.CharField(max_length=250)
    # address = models.TextField(null=True)
    address_line = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=200, null=True)
    phone = models.CharField(null=True, max_length=300)

    def __str__(self):
        return str(self.binfo_id)


class PaymentDetail(models.Model):
    detail_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    detail_instruction = models.TextField(blank=True)
    account_name = models.CharField(max_length=800, blank=True)
    account_no = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.detail_id)


class PaymentType(models.Model):
    types = [('cash', 'Cash'), ('bank', 'Bank Payment'),
             ('mob', 'Mobile Banking')]
    type_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    type_name = models.CharField(max_length=300)
    icon = models.FileField(upload_to='payment_method/pics', null=True)
    core_transaction_outlet = models.CharField(
        max_length=4, choices=types, null=True, blank=True)
    payment_detail = models.ForeignKey(PaymentDetail, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=False)

    def __str__(self):import random
from uuid import uuid4
from django.db import models
from products.models import Product
from accounts.models import CustomUser


class CartObject(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    anon_usr = models.CharField(max_length=300, null=True, unique=True)
    anonnymous = models.BooleanField(default=True)
    items = models.ManyToManyField(CartObject, blank=True)

    def __str__(self):
        return str(self.cart_id)


class BillingInfo(models.Model):
    binfo_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)

    full_name = models.CharField(max_length=250)
    # address = models.TextField(null=True)
    address_line = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=200, null=True)
    phone = models.CharField(null=True, max_length=300)

    def __str__(self):
        return str(self.binfo_id)


class PaymentDetail(models.Model):
    detail_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    detail_instruction = models.TextField(blank=True)
    account_name = models.CharField(max_length=800, blank=True)
    account_no = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.detail_id)


class PaymentType(models.Model):
    types = [('cash', 'Cash'), ('bank', 'Bank Payment'),
             ('mob', 'Mobile Banking')]
    type_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    type_name = models.CharField(max_length=300)
    icon = models.FileField(upload_to='payment_method/pics', null=True)
    core_transaction_outlet = models.CharField(
        max_length=4, choices=types, null=True, blank=True)
    payment_detail = models.ForeignKey(PaymentDetail, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.type_name


class Order(models.Model):
    products = models.ManyToManyField(CartObject, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    order_stats = [
        ('pen', 'Pending Order'),
        ('cmp', 'Completed Order'),
        ('can', 'Cancelled Order')
    ]
    core_order_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    order_id = models.CharField(max_length=500, null=True)
    billing_info = models.ForeignKey(
        BillingInfo, on_delete=models.CASCADE, null=True)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_status = models.CharField(
        max_length=10, choices=order_stats, default='pen')
    paid_already = models.BooleanField(default=False)
    reference_no = models.CharField(max_length=300, null=True, blank=True)
    payment_type = models.ForeignKey(
        PaymentType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        a = random.sample(range(10), 3)
        self.order_id = "#{}".format(int(str(random.randint(1, 9)) +
                                         str(a[0]) + str(a[1]) + str(a[2])))
        super(Order, self).save(*args, **kwargs)

        return self.type_name


class Order(models.Model):
    products = models.ManyToManyField(CartObject, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    order_stats = [
        ('pen', 'Pending Order'),
        ('cmp', 'Completed Order'),
        ('can', 'Cancelled Order')
    ]
    core_order_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    order_id = models.CharField(max_length=500, null=True)
    billing_info = models.ForeignKey(
        BillingInfo, on_delete=models.CASCADE, null=True)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_status = models.CharField(
        max_length=10, choices=order_stats, default='pen')
    paid_already = models.BooleanField(default=False)
    reference_no = models.CharField(max_length=300, null=True, blank=True)
    payment_type = models.ForeignKey(
        PaymentType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        a = random.sample(range(10), 3)
        self.order_id = "#{}".format(int(str(random.randint(1, 9)) +
                                         str(a[0]) + str(a[1]) + str(a[2])))
        super(Order, self).save(*args, **kwargs)
