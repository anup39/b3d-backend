import django_filters
from .models import Project
from .models import StandardCategory, SubCategory, Category ,CategoryStyle
from .models import GlobalSubCategory ,GlobalCategory
from .models import RasterData


# Project filter
class ProjectFilter(django_filters.FilterSet):
    owner = django_filters.CharFilter(field_name='owner')

    class Meta:
        model = Project
        fields = ['owner']

# Global Categories filter
class GlobalSubCategoryFilter(django_filters.FilterSet):
    standard_category_ids = django_filters.CharFilter(
        method='filter_by_standard_category_ids',
        label='Standard Category IDs',
    )

    class Meta:
        model = GlobalSubCategory
        fields = ['standard_category_ids']

    def filter_by_standard_category_ids(self, queryset, name, value):
        if value == "empty":
            return queryset.none()
        if not value:
            # If standard_category_ids parameter is empty or not provided, return an empty queryset.
            return queryset.none()

        standard_category_ids = value.split(',')
        return queryset.filter(standard_category__id__in=standard_category_ids)

class GlobalCategoryFilter(django_filters.FilterSet):
    standard_category_ids = django_filters.CharFilter(
        method='filter_by_standard_category_ids',
        label='Standard Category IDs',
    )
    sub_category_ids = django_filters.CharFilter(
        method='filter_by_sub_category_ids',
        label='Sub Category IDs',
    )

    class Meta:
        model = GlobalCategory
        fields = ['standard_category_ids' ,'sub_category_ids']

    def filter_by_standard_category_ids(self, queryset, name, value):
        if value == "empty":
            return queryset.none()
        if not value:
            # If standard_category_ids parameter is empty or not provided, return an empty queryset.
            return queryset.none()

        standard_category_ids = value.split(',')
        return queryset.filter(standard_category__id__in=standard_category_ids)
    
    def filter_by_sub_category_ids(self, queryset, name, value):
        if value == "empty":
            return queryset.none()
        if not value:
            # If standard_category_ids parameter is empty or not provided, return an empty queryset.
            return queryset.none()

        sub_category_ids = value.split(',')
        return queryset.filter(sub_category__id__in=sub_category_ids)
class StandardCategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    view_name = django_filters.CharFilter(field_name='view_name')


    class Meta:
        model = StandardCategory
        fields = ['project','view_name']


class SubCategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    standard_category = django_filters.CharFilter(field_name='standard_category__id')
    view_name = django_filters.CharFilter(field_name='view_name')

    class Meta:
        model = SubCategory
        fields = ['project','standard_category','view_name']

class CategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    sub_category = django_filters.CharFilter(field_name='sub_category__id')
    view_name = django_filters.CharFilter(field_name='view_name')


    class Meta:
        model = Category
        fields = ['project','sub_category','view_name']

class CategoryStyleFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    category = django_filters.CharFilter(field_name='category__id')

    class Meta:
        model = CategoryStyle
        fields = ['project','category']

class RasterDataFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    is_display = django_filters.BooleanFilter(field_name='is_display')


    class Meta:
        model= RasterData
        fields = ['project','is_display',]
