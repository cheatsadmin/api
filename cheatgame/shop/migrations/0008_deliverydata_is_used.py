# Generated by Django 4.0.7 on 2024-03-19 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverydata',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]