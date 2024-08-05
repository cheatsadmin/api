# Generated by Django 4.0.7 on 2024-03-04 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0010_alter_attachment_attachment_type_and_more'),
        ('shop', '0006_alter_deliverydata_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issue', '0002_delete_issue_delete_issuecategory_delete_issuereport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('picture', models.FileField(upload_to='')),
                ('title', models.CharField(max_length=150)),
                ('description', models.FileField(upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150)),
                ('issue_type', models.IntegerField(choices=[(1, 'CONSOLE'), (2, 'CONTROLLER')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IssueTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issue.issue')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issue.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IssueReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('delivery_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.deliverydata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IssueListReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issue.issue')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issue.issuereport')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IssueCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issue.issue')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]