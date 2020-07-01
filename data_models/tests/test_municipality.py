from data_models.models import Municipality
from django.test import TestCase


class MunicipalityTest(TestCase):
    def test_load_municipalities(self):
        # Checks that the data migrations worked
        self.assertEqual(len(Municipality.objects.all()), 99)
