from django.test import TestCase

from data_models.models import BBR, House

from .factories import add_houses


class CityTest(TestCase):
    def test_add_house_by_kvhx(self):
        kvhx = "05610484_103_______"
        self.assertEqual(House.objects.all().count(), 0)
        house = House.add_house(kvhx=kvhx)
        self.assertEqual(House.objects.all().count(), 1)
        self.assertEqual(house.zip_code, 6771)
        self.assertEqual(house.address, "Kjærmarken 103, 6771 Gredstedbro")
        self.assertEqual(house.municipality.name, "Esbjerg")
        house.delete()

    def test_add_house_by_address(self):
        address = "Glahns Alle 41 4. th 2000 Frederiksberg"
        self.assertEqual(House.objects.all().count(), 0)
        house = House.add_house(address_text=address)
        self.assertEqual(House.objects.all().count(), 1)
        self.assertEqual(house.zip_code, 2000)
        self.assertEqual(house.municipality.name, "Frederiksberg")
        house.delete()

    def test_add_houses(self):
        nr_houses = 10
        self.assertEqual(House.objects.all().count(), 0)
        add_houses(nr_houses)
        self.assertEqual(House.objects.all().count(), nr_houses)
        self.assertGreaterEqual(BBR.objects.all().count(), nr_houses)
