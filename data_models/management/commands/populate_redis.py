from django.core.management.base import BaseCommand

from data_models.visualizer.data_fetching import fill_redis


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        fill_redis()
