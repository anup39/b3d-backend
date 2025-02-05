# Generated by Django 4.2.3 on 2023-10-10 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_linestringdata_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorystyle',
            name='category',
            field=models.OneToOneField(blank=True, help_text='Geometry related to this Category', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.category', verbose_name='Category'),
        ),
    ]
