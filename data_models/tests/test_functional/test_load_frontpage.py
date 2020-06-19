import os
import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .functional_test_helpers import get_text_contains


"""
This test checks that the front page can be loaded without problems
"""


class FrontPageTest(StaticLiveServerTestCase):
    serialized_rollback = True  # Django bug https://stackoverflow.com/questions/31991573/data-migration-only-executed-for-the-first-test
    host = socket.gethostbyname(socket.gethostname())
    host = socket.gethostbyname(socket.gethostname())

    def setUp(self):
        self.browser = webdriver.Remote(
            "http://selenium:4444/wd/hub", DesiredCapabilities.CHROME
        )

    def tearDown(self):
        if not os.path.exists("test-screens"):
            os.mkdir("test-screens")
        self.browser.save_screenshot("test-screens/entry_page_test.png")
        self.browser.quit()

    def test_entry_page(self):
        self.assertEqual(1, 1)
        # Loads the login page
        self.browser.get(self.live_server_url)
        get_text_contains(self.browser, "Kommunekort")
