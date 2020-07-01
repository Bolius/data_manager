import os
import socket

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


"""
This test creates a super user and checks that the admin interface can be loaded
"""


class MunicipalityAdminTeest(StaticLiveServerTestCase):
    serialized_rollback = True  # Django bug https://stackoverflow.com/questions/31991573/data-migration-only-executed-for-the-first-test
    host = socket.gethostbyname(socket.gethostname())

    def setUp(self):
        self.password = "2ojvv421kLf4"
        self.name = "Torben Test"
        self.mail = "admin@example.com"
        self.admin = User.objects.create_superuser(self.name, self.mail, self.password)
        self.browser = webdriver.Remote(
            "http://selenium:4444/wd/hub", DesiredCapabilities.CHROME
        )

    def tearDown(self):
        if not os.path.exists("test-screens"):
            os.mkdir("test-screens")
        self.browser.save_screenshot("test-screens/admin_load_test.png")
        self.browser.quit()

    def test_municipality_admin(self):
        # Loads the admin login page
        self.browser.get(f"{self.live_server_url}/admin")
        self.assertIn("admin", self.browser.title)

        # Enter login details
        field = self.browser.find_element_by_name("username")
        field.send_keys(self.name)

        field = self.browser.find_element_by_name("password")
        field.send_keys(self.password)

        # Submit form
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

        # Check that we are logged in with welcome message in top right
        self.assertGreater(
            len(
                self.browser.find_elements_by_xpath(
                    "//*[text()[contains(.,'Velkommen')]]"
                )
            ),
            0,
        )

        # Check that municipality admin can load
        elment = self.browser.find_element_by_link_text("Kommuner")
        self.browser.get(elment.get_attribute("href"))
        try:
            WebDriverWait(self.browser, 10).until(EC.url_contains("municipality"))
        except Exception:
            self.fail("Could not reach person admin site")

        # GO to person change page
        elment = self.browser.find_element_by_link_text("Ballerup")
        self.browser.get(elment.get_attribute("href"))
        try:
            WebDriverWait(self.browser, 10).until(EC.url_contains("change"))
        except Exception:
            self.fail("Could not reach change municipality admin site")
