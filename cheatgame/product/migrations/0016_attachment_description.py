# Generated by Django 4.0.7 on 2024-05-24 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_product_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
