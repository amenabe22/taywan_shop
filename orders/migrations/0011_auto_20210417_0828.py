# Generated by Django 3.1.2 on 2021-04-17 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20210417_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttype',
            name='icon',
            field=models.FileField(null=True, upload_to='payment_method/pics'),
        ),
    ]
