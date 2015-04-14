import sys
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core import management


class FunctionalTest(StaticLiveServerTestCase):
    RANDY_FIRST_NAME = 'Randy'
    RANDY_LAST_NAME = 'Bachatero'
    RANDY_FULL_NAME = RANDY_FIRST_NAME + ' ' + RANDY_LAST_NAME
    RANDY_EMAIL = 'randy@example.com'
    RANDY_EDU_EMAIL = 'randy@example.edu'
    RANDY_PASSWORD = 'password'
    BOBBY_EMAIL = 'bobby@example.com'
    BOBBY_PASSWORD = 'password'

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
        management.call_command('loaddata', 'fixtures/common/colleges.json')
        management.call_command('loaddata', 'fixtures/common/dates.json')
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()
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

    def assert_text_in_page(self, text, case_insensitive=False):
        body_text = self.browser.find_element_by_tag_name('body').text
        if case_insensitive:
            text = text.lower()
            body_text = body_text.lower()
        self.assertTrue(text in body_text)

    class wait_for_page_load(object):

        def __init__(self, browser):
            self.browser = browser

        def __enter__(self):
            self.old_page = self.browser.find_element_by_tag_name('html')

        def page_has_loaded(self):
            new_page = self.browser.find_element_by_tag_name('html')
            return new_page.id != self.old_page.id

        def __exit__(self, *_):
            self.wait_for(self.page_has_loaded)

        def wait_for(self, condition_function):
            start_time = time.time()
            while time.time() < start_time + 3:
                if condition_function():
                    return True
                else:
                    time.sleep(0.1)
            raise Exception(
                'Timeout waiting for {}'.format(condition_function.__name__)
            )

    def logout(self):
        self.browser.find_element_by_link_text('Logout').click()
        self.assertNotIn('Logout', self.browser.find_element_by_id('cso-navbar').text)
        self.assertIn('You have signed out.', self.browser.find_element_by_tag_name('body').text)