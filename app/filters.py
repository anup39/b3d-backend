import django_filters
from .models import StandardCategory, SubCategory, Category ,CategoryStyle
from .models import GlobalSubCategory ,GlobalCategory


class StandardCategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')

    class Meta:
        model = StandardCategory
        fields = ['project']


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


class SubCategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    standard_category = django_filters.CharFilter(field_name='standard_category__id')
    class Meta:
        model = SubCategory
        fields = ['project','standard_category']



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

class CategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    sub_category = django_filters.CharFilter(field_name='sub_category__id')

    class Meta:
        model = Category
        fields = ['project','sub_category']

class CategoryStyleFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    category = django_filters.CharFilter(field_name='category__id')

    class Meta:
        model = CategoryStyle
        fields = ['project','category']