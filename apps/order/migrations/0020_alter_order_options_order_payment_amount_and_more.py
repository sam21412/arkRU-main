# Generated by Django 4.2.17 on 2025-01-08 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_order_payment_id_order_payment_method'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AddField(
            model_name='order',
            name='payment_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Payment Amount'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_currency',
            field=models.CharField(default='RUB', max_length=12, verbose_name='Payment Currency'),
        ),
    ]
