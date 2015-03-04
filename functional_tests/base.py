from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys
import os
from selenium import webdriver
from django.core import management


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg and 'dev' not in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        management.call_command('loaddata', 'fixtures/common/sites.json')
        management.call_command('loaddata', 'fixtures/initial_data-{}.json'.format(os.getenv('DJANGO_CONFIGURATION').lower()))
        management.call_command('loaddata', 'fixtures/extras/colleges.json')
        management.call_command('loaddata', 'fixtures/extras/dates.json')
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def click_link_assert_new_page(self, link):
        old_page = self.browser.page_source
        self.browser.find_element_by_link_text(link).click()
        new_page = self.browser.page_source
        self.assertHTMLNotEqual(old_page, new_page,
                                'Clicking the {} link has not sent the user to a new page.'.format(link))

    def switch_to_newest_window(self):
        self.browser.switch_to.window(self.browser.window_handles[-1])
