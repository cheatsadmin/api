# Generated by Django 4.0.7 on 2023-12-20 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
    ]