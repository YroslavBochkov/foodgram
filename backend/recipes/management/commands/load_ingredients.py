import csv

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из CSV в базу данных'

    def handle(self, *args, **options):
        self.import_ingredients()

    def import_ingredients(self, file='data/ingredients.csv'):
        """Импортирует ингредиенты из указанного CSV-файла."""
        file_path = '/Users/yaroslav/Dev/foodgram/data/ingredients.csv'

        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    name = row[0]
                    measurement_unit = row[1]
                    Ingredient.objects.update_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
            self.stdout.write(self.style.SUCCESS('Ингредиенты загружены.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке: {e}'))
