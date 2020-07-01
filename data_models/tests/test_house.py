from data_models.models import BBR, House
from django.test import TestCase

from .factories import add_houses


class CityTest(TestCase):
    def test_add_house_by_kvhx(self):
        kvhx = "05610484_103_______"
        self.assertEqual(House.objects.all().count(), 0)
        house = House.add_house_by_kvhx(kvhx)
        self.assertEqual(House.objects.all().count(), 1)
        self.assertEqual(house.zip_code, 6771)
        self.assertEqual(house.address, "Kjærmarken 103, 6771 Gredstedbro")

    def test_add_houses(self):
        nr_houses = 10
        self.assertEqual(House.objects.all().count(), 0)
        add_houses(nr_houses)
        self.assertEqual(House.objects.all().count(), nr_houses)
        self.assertGreaterEqual(BBR.objects.all().count(), nr_houses)
