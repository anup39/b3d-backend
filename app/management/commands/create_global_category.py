# app/management/commands/create_global_category.py

from django.core.management.base import BaseCommand
from django.db.models import Subquery, OuterRef
from app.models import PolygonData ,LineStringData, PointData ,Category

class Command(BaseCommand):
    help = 'Update global_category in PolygonData model from related Category model'

    def handle(self, *args, **options):
        # Subquery to get the global_category of the related Category
        subquery = Category.objects.filter(id=OuterRef('category_id')).values('global_category')[:1]

        # Update all PolygonData objects in a single query
        PolygonData.objects.update(global_category=Subquery(subquery))


        self.stdout.write(self.style.SUCCESS('Successfully updated global_category for all PolygonData objects'))

        PointData.objects.update(global_category=Subquery(subquery))

        self.stdout.write(self.style.SUCCESS('Successfully updated global_category for all PointData objects'))

        LineStringData.objects.update(global_category=Subquery(subquery))

        self.stdout.write(self.style.SUCCESS('Successfully updated global_category for all LineData objects'))

        # for point in PointData.objects.all():
        #     if point.category and point.category.global_category:
        #         point.global_category = point.category.global_category
        #         point.save()
        # self.stdout.write(self.style.SUCCESS('Successfully updated global_category for all PointData objects'))

        # for line in LineStringData.objects.all():
        #     if line.category and line.category.global_category:
        #         line.global_category = line.category.global_category
        #         line.save()
        # self.stdout.write(self.style.SUCCESS('Successfully updated global_category for all LineData objects'))