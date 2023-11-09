# Generated by Django 4.2.3 on 2023-11-08 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0030_alter_category_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project', models.ForeignKey(help_text='Project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project')),
                ('user', models.ForeignKey(help_text='User', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
