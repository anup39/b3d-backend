# Generated by Django 4.2.3 on 2023-11-11 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0055_alter_project_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='categorystyle',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='globalcategory',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='globalcategorystyle',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='globalstandardcategory',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='globalsubcategory',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='linestringdata',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='pointdata',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='polygondata',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='rasterdata',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='role',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='standardcategory',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='userproject',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_as_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='userrole',
            name='created_by',
            field=models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='roles_as_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AlterField(
            model_name='userproject',
            name='project',
            field=models.ForeignKey(help_text='Project', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects_as_user', to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(help_text='The person who created the project', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='roles_as_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Client name', max_length=255, verbose_name='Client name')),
                ('description', models.TextField(default='', help_text='More in-depth description of the Client', verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date', verbose_name='Created at')),
                ('is_display', models.BooleanField(default=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(help_text='The person who created', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients_as_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('user', models.ForeignKey(help_text='Client associated user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients_as_user', to=settings.AUTH_USER_MODEL, verbose_name='Client User')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
    ]
