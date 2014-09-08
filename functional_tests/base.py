from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
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
