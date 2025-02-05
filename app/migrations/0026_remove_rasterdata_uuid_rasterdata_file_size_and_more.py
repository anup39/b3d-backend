# Generated by Django 4.2.3 on 2023-10-27 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_categorystyle_global_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rasterdata',
            name='uuid',
        ),
        migrations.AddField(
            model_name='rasterdata',
            name='file_size',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rasterdata',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rasterdata',
            name='is_display',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rasterdata',
            name='progress',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rasterdata',
            name='status',
            field=models.CharField(default=1, help_text='Status for the task', max_length=255, verbose_name='Status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rasterdata',
            name='task_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
