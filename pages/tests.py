from django.test import TestCase
from django.core.urlresolvers import resolve
import pages


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/').func, pages.views.home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
