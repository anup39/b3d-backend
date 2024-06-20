# app/management/commands/create_global_category.py

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Displays a simple greeting'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Hello, World! I am running the command'))
