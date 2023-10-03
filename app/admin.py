from django.contrib import admin
from .models import Project
from .models import GlobalStandardCategory, GlobalCategory, GlobalSubCategory , GlobalCategoryStyle
# Register your models here.
admin.site.register(Project)
admin.site.register(GlobalStandardCategory)
admin.site.register(GlobalCategory)
admin.site.register(GlobalSubCategory)
admin.site.register(GlobalCategoryStyle)