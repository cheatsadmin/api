# Generated by Django 4.0.7 on 2023-12-01 11:21

import cheatgame.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_baseuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='verify_type',
            field=models.IntegerField(choices=[(1, 'PHONENUMBER'), (2, 'EMAIL')], default=cheatgame.users.models.VerifyType['PHONENUMBER']),
        ),
    ]