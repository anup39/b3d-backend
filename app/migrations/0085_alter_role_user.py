# Generated by Django 4.2.3 on 2024-04-15 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0084_role_client_role_group_role_project_role_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.ForeignKey(help_text='User associated with this role', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
