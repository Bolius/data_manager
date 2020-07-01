from django.test import TestCase

from data_models.models import BBR

from .factories import add_houses


class BBRTimeTest(TestCase):
    def test_add_get_time_data(self):
        houses = add_houses(nr_houses=3)
        houses = [h.buldings.first() for h in houses]
        [h1, h2, h3] = houses
        h1.construction_year = 1990
        h2.construction_year = 1992
        h3.construction_year = 1992
        h1.reconstruction_year = 1991
        h2.reconstruction_year = None
        h3.reconstruction_year = 1992
        [h.save() for h in houses]
        data = BBR.get_time_data()
        self.assertEqual([1990, 1991, 1992], data["time_range"])
        self.assertEqual([1, 1, 3], data["houses_per_year"])
        self.assertEqual([0, 1, 2], data["recon_per_year"])

    def test_get_rolling_avgs(self):
        houses = add_houses(nr_houses=3)
        houses = [h.buldings.first() for h in houses]
        [h1, h2, h3] = houses
        h1.construction_year = 1990
        h1.building_area = 50

        h2.construction_year = 1991
        h2.building_area = 100

        h3.construction_year = 1996
        h3.building_area = 150

        [h.save() for h in houses]
        data = BBR.get_rolling_avgs()
        self.assertEqual(list(range(1990, 1997)), data["time_range"])
        self.assertEqual(
            [75.0, 75.0, 75.0, 100.0, 150.0, 150.0, 150.0], data["bulding_area"]
        )
