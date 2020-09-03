from django.core.management.base import BaseCommand
from tqdm import tqdm

from data_models.models import House


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("id_file", type=str)

    def handle(self, *args, **options):
        add_ids(options["id_file"])


def add_ids(file):
    all_ids = set(House.objects.all().values("access_id"))
    with open(file, "r") as ids:
        for line in tqdm(ids):
            try:
                if len(line) > 10:
                    id = line[:-1]
                    if id not in all_ids:
                        House.add_house(access_id=id)
            except Exception as e:
                print(e)
                continue
