from django.test import LiveServerTestCase
from selenium import webdriver


class HomePageUp(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_all_static_pages_present(self):
        # Juan hears about a new salsa event: The Collegiate Salsa Open.
        # He goes to the website and sees "Collegiate Salsa Open" in the title.
        self.browser.get(self.live_server_url)
        self.assertIn('Collegiate Salsa Open', self.browser.title)

        self.fail('Finish the test!')
