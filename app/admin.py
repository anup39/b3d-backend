from django.contrib import admin
from .models import Project
from .models import GlobalStandardCategory, GlobalCategory, GlobalSubCategory , GlobalCategoryStyle
from app.models import StandardCategory, SubCategory, Category,CategoryStyle
# Register your models here.
admin.site.register(Project)
admin.site.register(GlobalStandardCategory)
admin.site.register(GlobalCategory)
admin.site.register(GlobalSubCategory)
admin.site.register(GlobalCategoryStyle)

admin.site.register(StandardCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(CategoryStyle)