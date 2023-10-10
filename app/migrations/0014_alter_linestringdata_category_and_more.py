# Generated by Django 4.2.3 on 2023-10-05 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_pointdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linestringdata',
            name='category',
            field=models.ForeignKey(default=1, help_text='Cateogyr related to this LineString', on_delete=django.db.models.deletion.PROTECT, to='app.category', verbose_name='Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='category',
            field=models.ForeignKey(default=1, help_text='Cateogyr related to this Point', on_delete=django.db.models.deletion.PROTECT, to='app.category', verbose_name='Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='category',
            field=models.ForeignKey(default=1, help_text='Cateogyr related to this polygon', on_delete=django.db.models.deletion.PROTECT, to='app.category', verbose_name='Category'),
            preserve_default=False,
        ),
    ]
