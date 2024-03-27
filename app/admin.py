from django.contrib import admin
from .models import Client
from .models import Project
from .models import ProjectPolygon
from .models import GlobalStandardCategory, GlobalCategory, GlobalSubCategory, GlobalCategoryStyle
from .models import StandardCategory, SubCategory, Category, CategoryStyle
from .models import PolygonData, LineStringData, PointData
from .models import RasterData
from .models import Role, UserRole
from .models import OBJData
from .models import StandardInspection, SubInspection, Inspection
from .models import InspectionReport, InspectionPhoto, InpsectionPhotoGeometry


class BaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project')
    list_filter = ('client', 'project')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', )
    list_filter = ('client',)


models = [
    UserRole,
    ProjectPolygon,
    RasterData,
    StandardCategory, SubCategory, Category, CategoryStyle,
    PolygonData, LineStringData, PointData,
    InspectionReport,
]

for model in models:
    ModelAdmin = type(f'{model.__name__}Admin', (BaseAdmin,), {})
    try:
        admin.site.register(model, ModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass


admin.site.register(Client)
admin.site.register(Project, ProjectAdmin)
admin.site.register(GlobalStandardCategory)
admin.site.register(GlobalCategory)
admin.site.register(GlobalSubCategory)
admin.site.register(GlobalCategoryStyle)


admin.site.register(Role)
admin.site.register(OBJData)

admin.site.register(StandardInspection)
admin.site.register(SubInspection)
admin.site.register(Inspection)

admin.site.register(InspectionPhoto)
admin.site.register(InpsectionPhotoGeometry)
