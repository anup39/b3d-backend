# Generated by Django 4.2.3 on 2023-10-10 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_categorystyle_global_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linestringdata',
            name='project',
            field=models.ForeignKey(help_text='LineString related to the project', on_delete=django.db.models.deletion.DO_NOTHING, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='linestringdata',
            name='standard_category',
            field=models.ForeignKey(blank=True, help_text='Standard Category related to the LineString', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='linestringdata',
            name='sub_category',
            field=models.ForeignKey(blank=True, help_text='Sub Category related to the LineString', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.subcategory', verbose_name='Sub Category'),
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='project',
            field=models.ForeignKey(help_text='Point related to the project', on_delete=django.db.models.deletion.DO_NOTHING, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='standard_category',
            field=models.ForeignKey(blank=True, help_text='Standard Category related to the Point', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='sub_category',
            field=models.ForeignKey(blank=True, help_text='Sub Category related to the Point', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.subcategory', verbose_name='Sub Category'),
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='project',
            field=models.ForeignKey(help_text='Polygon related to the project', on_delete=django.db.models.deletion.DO_NOTHING, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='standard_category',
            field=models.ForeignKey(blank=True, help_text='Standard Category related to the polygon', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='sub_category',
            field=models.ForeignKey(blank=True, help_text='Sub Category related to the polygon', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.subcategory', verbose_name='Sub Category'),
        ),
    ]
