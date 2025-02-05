# Generated by Django 4.2.3 on 2023-10-03 12:46

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_globalcategory_sub_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='In which category you want to seperate your project layer', max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', help_text='Description about this category', verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date', verbose_name='Created at')),
                ('publised', models.BooleanField(default=False)),
                ('view_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('is_display', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('project', models.ForeignKey(help_text='Category related to the project', on_delete=django.db.models.deletion.PROTECT, to='app.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='StandardCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='In which standard category you want to seperate your project layer', max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', help_text='Description about this category', verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date', verbose_name='Created at')),
                ('publised', models.BooleanField(default=False)),
                ('view_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('is_display', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('project', models.ForeignKey(help_text='Standard Category related to the project', on_delete=django.db.models.deletion.PROTECT, to='app.project', verbose_name='Project')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='In which Sub category you want to seperate your project layer', max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', help_text='Description about this category', verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date', verbose_name='Created at')),
                ('publised', models.BooleanField(default=False)),
                ('view_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('is_display', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('project', models.ForeignKey(help_text='Sub Category related to the project', on_delete=django.db.models.deletion.PROTECT, to='app.project', verbose_name='Project')),
                ('standard_category', models.ForeignKey(help_text='Standard Category related to the project', on_delete=django.db.models.deletion.PROTECT, to='app.standardcategory', verbose_name='Standard Category')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date', verbose_name='Created at')),
                ('fill', colorfield.fields.ColorField(default='#2c3e50', help_text='Fill color for the polygon', image_field=None, max_length=25, samples=None, verbose_name='Fill Color')),
                ('fill_opacity', models.DecimalField(decimal_places=2, default=0.5, max_digits=3)),
                ('stroke', colorfield.fields.ColorField(default='#ffffff', help_text='Stroke coloe for the polygon', image_field=None, max_length=25, samples=None, verbose_name='Stroke Color')),
                ('stroke_width', models.PositiveIntegerField(default=1)),
                ('xml', models.TextField(blank=True, null=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.OneToOneField(help_text='Geometry related to this Category', on_delete=django.db.models.deletion.PROTECT, to='app.category', verbose_name='Category')),
                ('project', models.ForeignKey(help_text='Style related to the project', on_delete=django.db.models.deletion.PROTECT, to='app.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'CategoryStyle',
                'verbose_name_plural': 'CategoryStyles',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='standard_category',
            field=models.ForeignKey(help_text='Standard Category related to the project', on_delete=django.db.models.deletion.PROTECT, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AddField(
            model_name='category',
            name='sub_category',
            field=models.ForeignKey(help_text='Sub Category related to the project', on_delete=django.db.models.deletion.PROTECT, to='app.subcategory', verbose_name='Sub Category'),
        ),
    ]
