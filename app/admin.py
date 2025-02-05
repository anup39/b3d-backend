from django.contrib import admin
from .models import Client
from .models import Project
from .models import ProjectPolygon
from .models import GlobalStandardCategory, GlobalCategory, GlobalSubCategory, GlobalCategoryStyle
from .models import StandardCategory, SubCategory, Category, CategoryStyle
from .models import PolygonData, LineStringData, PointData
from .models import RasterData
from .models import Role
from .models import OBJData
from .models import StandardInspection, SubInspection, Inspection
from .models import InspectionReport, InspectionPhoto, InpsectionPhotoGeometry
from .models import MeasuringFileUpload
from .models import Indoor


class BaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project')
    list_filter = ('client', 'project' ,)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', )
    list_filter = ('client',)


class StandardCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project', 'name', 'view_name')
    list_filter = ('client', 'project')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project', 'name', 'view_name')
    list_filter = ('client', 'project')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project', 'name', 'view_name')
    list_filter = ('client', 'project')


class CategoryStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project', 'category')
    list_filter = ('client', 'project')

class PolygonDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project', 'standard_category', 'sub_category', 'global_category','category' ,"extra_fields")
    list_filter = ( 'client', 'project', 'standard_category', 'sub_category', 'global_category','category')

class LineStringDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project', 'standard_category', 'sub_category', 'global_category','category',"extra_fields")
    list_filter = ( 'client', 'project', 'standard_category', 'sub_category', 'global_category','category')

class PointDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project', 'standard_category', 'sub_category', 'global_category','category',"extra_fields")
    list_filter = ( 'client', 'project', 'standard_category', 'sub_category', 'global_category','category')

class GlobalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'extra_fields')
   


class RoleAdmin(admin.ModelAdmin):
    list_filter = ('user',)


models = [
    ProjectPolygon,
    RasterData,
    # StandardCategory, SubCategory, Category, CategoryStyle,
    # PolygonData, LineStringData, PointData,
    InspectionReport,
]

for model in models:
    ModelAdmin = type(f'{model.__name__}Admin', (BaseAdmin,), {})
    try:
        admin.site.register(model, ModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass


admin.site.register(StandardCategory, StandardCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryStyle, CategoryStyleAdmin)


admin.site.register(Client)
admin.site.register(Project, ProjectAdmin)
admin.site.register(GlobalStandardCategory)
admin.site.register(GlobalCategory, GlobalCategoryAdmin)
admin.site.register(GlobalSubCategory)
admin.site.register(GlobalCategoryStyle)


admin.site.register(Role, RoleAdmin)
admin.site.register(OBJData)

admin.site.register(StandardInspection)
admin.site.register(SubInspection)
admin.site.register(Inspection)

admin.site.register(InspectionPhoto)
admin.site.register(InpsectionPhotoGeometry)

admin.site.register(MeasuringFileUpload)
admin.site.register(Indoor)

admin.site.register(PolygonData, PolygonDataAdmin)
admin.site.register(LineStringData, LineStringDataAdmin)
admin.site.register(PointData, PointDataAdmin)

