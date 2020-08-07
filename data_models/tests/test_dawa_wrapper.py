from django.test import TestCase

from data_models.api_wrappers import address_to_kvhx


class DataHandlerTestCase(TestCase):
    def test_address_to_kvhx(self):
        address = "glahns alle 41 4. th, 2000 Frederiksberg"
        expected_kvhx = "01470310__41__4__th"
        actual_kvhx = address_to_kvhx(address)
        self.assertEqual(expected_kvhx, actual_kvhx)

    def test_address_to_kvhx_invalid_address(self):
        wrong_address = "glahns all 41, 2000 Frederiksberg"
        self.assertRaises(ValueError, lambda: address_to_kvhx(wrong_address))
