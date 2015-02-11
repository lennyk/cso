from .base import FunctionalTest
from unittest import skip


class HomePageUp(FunctionalTest):

    def test_all_static_pages_present(self):
        # Juan hears about a new salsa event: The Collegiate Salsa Open.
        # He goes to the website and sees "Collegiate Salsa Open" in the title.
        self.browser.get(self.server_url)
        self.assertIn('Collegiate Salsa Open', self.browser.title)

        # Juan sees there is plenty of information about CSO in a menu with various links.
        pages = ['Home', 'Event Information', 'Colleges', 'About']
        nav_links = self.browser.find_elements_by_css_selector('ul.nav > li > a')
        for page in pages:
            print(['a link: {}'.format(nav_link.text) for nav_link in nav_links])
            self.assertIn(page.lower(), [nav_link.text.lower() for nav_link in nav_links])

        # Juan can click the navigation link labeled Event Information
        self.browser.find_element_by_link_text('Event Information').click()

        # Juan can click the navigation link labeled Colleges
        self.browser.find_element_by_link_text('Colleges').click()

        # Juan can click the navigation link labeled About
        self.browser.find_element_by_link_text('About').click()

        # Juan can click the navigation link labeled Home
        self.browser.find_element_by_link_text('Home').click()

        # Juan sees the Home section
        self.assertTrue(self.browser.find_element_by_id('home').is_displayed())

        # Juan sees the Event Information section
        self.assertTrue(self.browser.find_element_by_id('event').is_displayed())

        # Juan sees the Colleges section
        self.assertTrue(self.browser.find_element_by_id('colleges').is_displayed())

        # Juan sees the About section
        self.assertTrue(self.browser.find_element_by_id('about').is_displayed())
