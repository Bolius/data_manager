from django.core.management.base import BaseCommand
from tqdm import tqdm

from data_models.models import House


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("id_file", type=str)

    def handle(self, *args, **options):
        with open(options["id_file"], "r") as ids:
            for line in tqdm(ids):
                try:
                    if len(line) > 10:
                        House.add_house(access_id=line[:-1])
                except Exception as e:
                    print(e)
                    continue

        #
        # for poll_id in options["poll_ids"]:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(
        #         self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
        #     )
