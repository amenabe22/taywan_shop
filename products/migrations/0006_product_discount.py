# Generated by Django 3.1.2 on 2021-04-29 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.BigIntegerField(blank=True, help_text='Discount percentage for product sales', null=True),
        ),
    ]