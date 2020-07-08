from django.test import TestCase

from data_models.models import House, Municipality


class MunicipalityTest(TestCase):
    TOTAL_MUNICIPALITIES = 99

    @classmethod
    def setUpClass(cls):
        h1 = "05610484_103_______"  # Kjærmarken 103, 6771 Gredstedbro, muni: Esbjerg
        h2 = "0a3f50a2-4ea4-32b8-e044-0003ba298018"  # Jarmers Plads
        cls.h1 = House.add_house(kvhx=h1)
        cls.h2 = House.add_house(access_id=h2)

    @classmethod
    def tearDownClass(cls):
        cls.h1.delete()
        cls.h2.delete()

    def test_load_municipalities(self):
        # Checks that the data migrations worked
        self.assertEqual(len(Municipality.objects.all()), self.TOTAL_MUNICIPALITIES)

    def test_get_stats(self):
        stats = Municipality.get_stats()
        self.assertEqual(stats[self.h1.municipality.admin_code]["nr_houses"], 1)
        self.assertEqual(stats[self.h2.municipality.admin_code]["nr_houses"], 1)
        self.assertEqual(len(stats), self.TOTAL_MUNICIPALITIES)
