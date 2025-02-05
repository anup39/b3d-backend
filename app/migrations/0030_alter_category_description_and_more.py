# Generated by Django 4.2.3 on 2023-11-08 02:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0029_role_userrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='', help_text='Description about this category', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='global_category',
            field=models.ForeignKey(help_text='Global Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalcategory', verbose_name='Global  Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='global_standard_category',
            field=models.ForeignKey(help_text='Global Standard Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalstandardcategory', verbose_name='Global Standard Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='global_sub_category',
            field=models.ForeignKey(help_text='Global Sub Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalsubcategory', verbose_name='Global Sub Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='project',
            field=models.ForeignKey(help_text='Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='category',
            name='standard_category',
            field=models.ForeignKey(help_text='Standard Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='sub_category',
            field=models.ForeignKey(help_text='Sub Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.subcategory', verbose_name='Sub Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='view_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='categorystyle',
            name='category',
            field=models.OneToOneField(help_text='Geometry related to this Category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='categorystyle',
            name='global_category',
            field=models.OneToOneField(help_text='Geometry related to this Category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalcategory', verbose_name='Global Category'),
        ),
        migrations.AlterField(
            model_name='categorystyle',
            name='project',
            field=models.ForeignKey(help_text='Style related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='categorystyle',
            name='xml',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='globalcategory',
            name='description',
            field=models.TextField(default='', help_text='Description about this category', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='globalcategory',
            name='standard_category',
            field=models.ForeignKey(help_text='Standard Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalstandardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='globalcategory',
            name='sub_category',
            field=models.ForeignKey(help_text='Sub Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalsubcategory', verbose_name='Sub Category'),
        ),
        migrations.AlterField(
            model_name='globalcategorystyle',
            name='category',
            field=models.OneToOneField(help_text='Style related to this Category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalcategory', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='globalcategorystyle',
            name='xml',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='globalstandardcategory',
            name='description',
            field=models.TextField(default='', help_text='Description about this category', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='globalsubcategory',
            name='description',
            field=models.TextField(default='', help_text='Description about this category', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='globalsubcategory',
            name='standard_category',
            field=models.ForeignKey(help_text='Standard Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalstandardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='linestringdata',
            name='attributes',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='linestringdata',
            name='category',
            field=models.ForeignKey(help_text='Cateogyr related to this LineString', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='linestringdata',
            name='project',
            field=models.ForeignKey(help_text='LineString related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='linestringdata',
            name='standard_category',
            field=models.ForeignKey(help_text='Standard Category related to the LineString', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='linestringdata',
            name='sub_category',
            field=models.ForeignKey(help_text='Sub Category related to the LineString', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.subcategory', verbose_name='Sub Category'),
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='attributes',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='category',
            field=models.ForeignKey(help_text='Cateogyr related to this Point', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='project',
            field=models.ForeignKey(help_text='Point related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='standard_category',
            field=models.ForeignKey(help_text='Standard Category related to the Point', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='pointdata',
            name='sub_category',
            field=models.ForeignKey(help_text='Sub Category related to the Point', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.subcategory', verbose_name='Sub Category'),
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='attributes',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='category',
            field=models.ForeignKey(help_text='Cateogyr related to this polygon', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='project',
            field=models.ForeignKey(help_text='Polygon related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='standard_category',
            field=models.ForeignKey(help_text='Standard Category related to the polygon', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='polygondata',
            name='sub_category',
            field=models.ForeignKey(help_text='Sub Category related to the polygon', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.subcategory', verbose_name='Sub Category'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(default='', help_text='More in-depth description of the project', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(help_text='The person who created the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.TextField(db_index=True, default='', help_text='Project tags', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='rasterdata',
            name='project',
            field=models.ForeignKey(help_text='Point related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='rasterdata',
            name='task_id',
            field=models.UUIDField(null=True),
        ),
        migrations.AlterField(
            model_name='standardcategory',
            name='description',
            field=models.TextField(default='', help_text='Description about this category', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='standardcategory',
            name='global_standard_category',
            field=models.ForeignKey(help_text='Global Standard Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalstandardcategory', verbose_name='Global Standard Category'),
        ),
        migrations.AlterField(
            model_name='standardcategory',
            name='project',
            field=models.ForeignKey(help_text='Standard Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='standardcategory',
            name='view_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='description',
            field=models.TextField(default='', help_text='Description about this category', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='global_standard_category',
            field=models.ForeignKey(help_text='Global Standard Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalstandardcategory', verbose_name='Global Standard Category'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='global_sub_category',
            field=models.ForeignKey(help_text='Global Sub Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.globalsubcategory', verbose_name='Global Sub Category'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='project',
            field=models.ForeignKey(help_text='Sub Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='standard_category',
            field=models.ForeignKey(help_text='Standard Category related to the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.standardcategory', verbose_name='Standard Category'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='view_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.ForeignKey(help_text='Role of the user', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.role', verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(help_text='The person who created the project', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
