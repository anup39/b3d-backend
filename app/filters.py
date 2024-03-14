import django_filters
from .models import Project, ProjectPolygon
from .models import StandardCategory, SubCategory, Category, CategoryStyle
from .models import GlobalSubCategory, GlobalCategory, GlobalCategoryStyle
from .models import RasterData
from .models import UserRole


# Project filter
class ProjectFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name='id')
    client = django_filters.CharFilter(field_name='client__id')

    class Meta:
        model = Project
        fields = ['id', 'client']

# Global Categories filter


class ProjectPolygonFilter(django_filters.FilterSet):
    client = django_filters.CharFilter(field_name='client__id')
    project = django_filters.CharFilter(field_name='project__id')

    class Meta:
        model = ProjectPolygon
        fields = ['project', 'client']


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
        fields = ['standard_category_ids', 'sub_category_ids']

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


class GlobalCategoryStyleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__id')

    class Meta:
        model = GlobalCategoryStyle
        fields = ['category',]


class StandardCategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    view_name = django_filters.CharFilter(field_name='view_name')
    client = django_filters.CharFilter(field_name='client__id')

    class Meta:
        model = StandardCategory
        fields = ['project', 'view_name', 'client',]


class SubCategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    standard_category = django_filters.CharFilter(
        field_name='standard_category__id')
    view_name = django_filters.CharFilter(field_name='view_name')
    client = django_filters.CharFilter(field_name='client__id')

    class Meta:
        model = SubCategory
        fields = ['project', 'standard_category', 'view_name', 'client']


class CategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    sub_category = django_filters.CharFilter(field_name='sub_category__id')
    view_name = django_filters.CharFilter(field_name='view_name')
    client = django_filters.CharFilter(field_name='client__id')

    class Meta:
        model = Category
        fields = ['project', 'sub_category', 'view_name', 'client']


class CategoryStyleFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    category = django_filters.CharFilter(field_name='category__id')
    client = django_filters.CharFilter(field_name='client__id')

    class Meta:
        model = CategoryStyle
        fields = ['project', 'category', 'client']


class RasterDataFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    is_display = django_filters.BooleanFilter(field_name='is_display')
    client = django_filters.CharFilter(field_name='client__id')

    class Meta:
        model = RasterData
        fields = ['project', 'is_display', 'client']


class UserRoleFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__id')
    client = django_filters.CharFilter(field_name='client__id')
    project = django_filters.CharFilter(field_name='project__id')
    properti = django_filters.CharFilter(field_name='properti__id')

    class Meta:
        model = UserRole
        fields = ['user', 'client', 'project', 'properti']
