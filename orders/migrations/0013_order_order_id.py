# Generated by Django 3.1.2 on 2021-04-17 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_paymenttype_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=500, null=True),
        ),
    ]