from django.test import TestCase

from data_models.models import BBR
from data_models.tests.factories import add_houses
from data_models.visualizer.data_fetching.fetch_scatter_data import compute_scatter_data


class FetchScatterDataTest(TestCase):
    def setUp(self):
        self.assertEqual(BBR.objects.all().count(), 0)
        self.houses = add_houses(nr_houses=3)

        [h1, h2, h3] = self.houses
        [b1, b2, b3] = [h.buldings.first() for h in self.houses]
        self.buldings = [b1, b2, b3]
        b1.construction_year = 1336
        b2.construction_year = 1337
        b3.construction_year = 1337

        b1.building_area = 420
        b2.building_area = 314
        b3.building_area = 314

        [h.save() for h in self.houses]
        [b.save() for b in self.buldings]

    def tearDown(self):
        [b.delete() for b in self.buldings]
        [h.delete() for h in self.houses]

    def test_area_year(self):
        actual = compute_scatter_data()
        expected = {
            "construction_years": [
                {"construction_year": 1336, "count": 1},
                {"construction_year": 1337, "count": 2},
            ],
            "building_areas": [
                {"building_area": 314, "count": 2},
                {"building_area": 420, "count": 1},
            ],
        }
        self.assertEqual(expected["construction_years"], actual["construction_years"])
        self.assertEqual(expected["building_areas"], actual["building_areas"])
