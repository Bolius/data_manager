from django.test import TestCase

from data_models.models import BBR, House

from .factories import add_houses


class BBRTimeTest(TestCase):
    def test_add_get_time_data(self):
        houses = add_houses(nr_houses=3)
        houses = [h.buldings.first() for h in houses]
        [h1, h2, h3] = houses
        h1.construction_year = 1990
        h2.construction_year = 1992
        h3.construction_year = 1992
        [h.save() for h in houses]
        data = BBR.get_time_data()
        self.assertEqual([1990, 1991, 1992], data["time_range"])
        self.assertEqual({1990: 1, 1991: 1, 1992: 3}, data["houses_per_year"])
