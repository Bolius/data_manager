from django.test import TestCase

from data_models.management.commands.add_addresses import add_ids
from data_models.models import House


class Add_commands_Test(TestCase):
    id_file = "data_models/tests/test_commands/tests_ids.txt"

    def setUp(self):
        with open(self.id_file) as idFile:
            self.ids = [
                line.replace("\n", "") for line in idFile.readlines() if len(line) > 5
            ]
            self.nr_to_add = len(self.ids)

    def tearDown(self):
        [h.delete() for h in House.objects.filter(access_id__in=self.ids)]

    def test_add_addresses(self):
        current_houses = House.objects.all().count()
        add_ids(self.id_file)
        self.assertEqual(current_houses + self.nr_to_add, House.objects.all().count())
