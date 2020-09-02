from django.test import TestCase

from data_models.visualizer.data_fetching import (
    accumulated_sum_for_catatgorical,
    compute_time_data,
)

from .factories import add_houses


class BBRTimeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.addresses = add_houses(nr_houses=3)
        cls.houses = [h.buldings.first() for h in cls.addresses]
        cls.h1 = cls.houses[0]
        cls.h2 = cls.houses[1]
        cls.h3 = cls.houses[2]

    @classmethod
    def tearDownClass(cls):
        [h.delete() for h in cls.houses]
        [a.delete() for a in cls.addresses]

    def test_add_get_time_data(self):
        self.h1.construction_year = 1990
        self.h2.construction_year = 1992
        self.h3.construction_year = 1992
        self.h1.reconstruction_year = 1991
        self.h2.reconstruction_year = None
        self.h3.reconstruction_year = 1992
        [h.save() for h in self.houses]
        data = compute_time_data()["time"]
        self.assertEqual([1990, 1991, 1992], data["time_range"])
        self.assertEqual([1, 1, 3], data["houses_per_year"])
        self.assertEqual([0, 1, 2], data["recon_per_year"])

    def test_get_rolling_avgs(self):
        self.h1.construction_year = 1990
        self.h1.building_area = 50

        self.h2.construction_year = 1991
        self.h2.building_area = 100

        self.h3.construction_year = 1996
        self.h3.building_area = 150

        [h.save() for h in self.houses]
        data = compute_time_data()["rolling_avgs"]
        self.assertEqual(list(range(1990, 1997)), data["time_range"])
        self.assertEqual(
            [75.0, 100.0, 100.0, 100.0, 100.0, 100.0, 125.0], data["bulding_area"]
        )

    def test_accumulated_sum_for_catatgorical(self):
        self.h1.construction_year = 1990
        self.h1.kitchen_facility = "E"

        self.h2.construction_year = 1991
        self.h2.kitchen_facility = "E"

        self.h3.construction_year = 1992
        self.h3.kitchen_facility = "F"

        [h.save() for h in self.houses]
        expected = [
            {"0": 0, "E": 1, "F": 0, "G": 0, "H": 0},
            {"0": 0, "E": 2, "F": 0, "G": 0, "H": 0},
            {"0": 0, "E": 2, "F": 1, "G": 0, "H": 0},
        ]
        actual = accumulated_sum_for_catatgorical("kitchen_facility", 1990, 1992)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0], actual[0])
        self.assertEqual(expected, actual)
