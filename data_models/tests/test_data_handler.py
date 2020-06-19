from django.test import TestCase

# from data_models.data_handlers import kvhToHouse, kvhToBBR, addressToKVH
from . import get_test_addresses


class DataHandlerTestCase(TestCase):
    def setUp(self):
        self.addresses = get_test_addresses()

    def testKvhToHouse(self):
        return None
        # for address in self.addresses:
        #     house = kvhToHouse(address["kvh"])
        #     self.assertEqual(house.address, address["address"])

    def testKvhToBBR(self):
        return None
        # for address in self.addresses:
        #     BBR = kvhToBBR(address["kvh"])
        #     self.assertEqual(
        #         BBR["bbr"]["values"]["unadr_bbrid"], address["unadr_bbrid"]
        #     )

    def testAddressToKvh(self):
        return None
        # for address in self.addresses:
        #     kvh = addressToKVH(address["address"])
        #     self.assertEqual(kvh.replace(" ", ""), address["kvh"])
