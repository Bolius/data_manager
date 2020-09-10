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
    all_ids = set(House.objects.all().values_list("dawa_id", flat=True))
    with open(file, "r") as ids:
        lines = [line[:-1] for line in ids.readlines() if len(line) > 10]
        lines = [line for line in lines if line not in all_ids]
    print(f"Already has {len(all_ids) - len(lines)} in data set")
    for line in tqdm(lines):
        try:
            House.add_house(access_id=line)
        except Exception as e:
            print(e)
            continue
