import django_filters
from .models import StandardCategory, SubCategory, Category ,CategoryStyle


class StandardCategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')

    class Meta:
        model = StandardCategory
        fields = ['project']

class SubCategoryFilter(django_filters.FilterSet):
    project = django_filters.CharFilter(field_name='project__id')
    standard_category = django_filters.CharFilter(field_name='standard_category__id')

    class Meta:
        model = SubCategory
        fields = ['project','standard_category']


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