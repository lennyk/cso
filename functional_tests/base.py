from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class HomePageUp(StaticLiveServerTestCase):

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

    def test_all_static_pages_present(self):
        # Juan hears about a new salsa event: The Collegiate Salsa Open.
        # He goes to the website and sees "Collegiate Salsa Open" in the title.
        self.browser.get(self.live_server_url)
        self.assertIn('Collegiate Salsa Open', self.browser.title)

        # Juan sees there is plenty of information about CSO in a menu with various links.
        pages = ['Home', 'About', 'Dates', 'Colleges']
        nav_links = self.browser.find_elements_by_css_selector('ul.nav > li > a')
        for page in pages:
            print(['a link: {}'.format(nav_link.text) for nav_link in nav_links])
            self.assertIn(page.lower(), [nav_link.text.lower() for nav_link in nav_links])

        # Juan clicks the dropdown navigation labeled About
        self.browser.find_element_by_link_text('About').click()

        # Juan clicks the link for the The CSO page and is taken to a new page.
        self.click_link_assert_new_page('The LDA')

        # Juan clicks the dropdown navigation labeled About
        self.browser.find_element_by_link_text('About').click()

        # Juan clicks the link for the Constitution page and is taken to a new page.
        self.click_link_assert_new_page('Constitution')

        # Juan clicks the link for the Dates page and is taken to a new page.
        self.click_link_assert_new_page('Dates')

        # Juan clicks the link for the Colleges page and is taken to a new page.
        self.click_link_assert_new_page('Colleges')
