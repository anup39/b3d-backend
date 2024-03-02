from django.contrib import admin
from .models import Client
from .models import Project
from .models import GlobalStandardCategory, GlobalCategory, GlobalSubCategory, GlobalCategoryStyle
from .models import StandardCategory, SubCategory, Category, CategoryStyle
from .models import PolygonData, LineStringData, PointData
from .models import RasterData
from .models import Role, UserRole
from .models import OBJData
from .models import StandardInspection, SubInspection, Inspection
from .models import InspectionReport, InspectionPhoto, InpsectionPhotoGeometry

# Register your models here.
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(GlobalStandardCategory)
admin.site.register(GlobalCategory)
admin.site.register(GlobalSubCategory)
admin.site.register(GlobalCategoryStyle)

admin.site.register(StandardCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(CategoryStyle)

admin.site.register(PolygonData)
admin.site.register(LineStringData)
admin.site.register(PointData)
admin.site.register(RasterData)

admin.site.register(Role)
admin.site.register(UserRole)

admin.site.register(OBJData)

admin.site.register(StandardInspection)
admin.site.register(SubInspection)
admin.site.register(Inspection)

admin.site.register(InspectionReport)
admin.site.register(InspectionPhoto)
admin.site.register(InpsectionPhotoGeometry)
