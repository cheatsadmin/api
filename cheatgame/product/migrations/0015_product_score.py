# Generated by Django 4.0.7 on 2024-05-24 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_reviews_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='score',
            field=models.DecimalField(decimal_places=2, default=4.8, max_digits=4),
        ),
    ]