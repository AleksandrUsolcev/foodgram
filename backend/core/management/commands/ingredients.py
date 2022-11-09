import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import CSV data for Ingredients'

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            type=str,
            help='Ingredients file path'
        )

    def handle(self, *args, **kwargs):
        path = kwargs.get('path')
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            count = 0
            for row in reader:
                count += 1
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
            print(f'Import {count} ingredients completed successfully')
