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
            [75.0, 100.0, 100.0, 100.0, 100.0, 100.0, 125.0], data["bulding_area"]
        )

    def test_accumulated_sum_for_catatgorical(self):
        houses = add_houses(nr_houses=3)
        houses = [h.buldings.first() for h in houses]
        [h1, h2, h3] = houses
        h1.construction_year = 1990
        h1.kitchen_facility = "E"

        h2.construction_year = 1991
        h2.kitchen_facility = "E"

        h3.construction_year = 1992
        h3.kitchen_facility = "F"

        [h.save() for h in houses]
        expected = [
            {"0": 0, "E": 1, "F": 0, "G": 0, "H": 0},
            {"0": 0, "E": 2, "F": 0, "G": 0, "H": 0},
            {"0": 0, "E": 2, "F": 1, "G": 0, "H": 0},
        ]
        actual = BBR.accumulated_sum_for_catatgorical("kitchen_facility", 1990, 1992)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0], actual[0])
        self.assertEqual(expected, actual)
