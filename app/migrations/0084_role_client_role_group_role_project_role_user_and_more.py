# Generated by Django 4.2.3 on 2024-04-15 01:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0083_linestringdata_task_id_pointdata_task_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='client',
            field=models.ForeignKey(help_text='Client associated with this role', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.client', verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='role',
            name='group',
            field=models.ForeignKey(help_text='Group associated with this role', null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='role',
            name='project',
            field=models.ManyToManyField(help_text='Project associated with this role', to='app.project', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='role',
            name='user',
            field=models.OneToOneField(help_text='User associated with this role', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(default='my_role', help_text='Name of the Role', max_length=255, verbose_name='Name'),
        ),
        migrations.DeleteModel(
            name='UserRole',
        ),
    ]
