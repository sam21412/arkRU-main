# Generated by Django 4.2.17 on 2025-01-04 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0028_attributeoption_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributeoption',
            name='price',
        ),
    ]
