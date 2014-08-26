from django.test import TestCase
from django.core.urlresolvers import resolve
import pages


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/').func, pages.views.home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class AboutPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/about/').func, pages.views.about_page)

    def test_uses_about_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'about.html')


class ConstitutionPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/about/constitution/').func, pages.views.constitution_page)

    def test_uses_about_template(self):
        response = self.client.get('/about/constitution/')
        self.assertTemplateUsed(response, 'constitution.html')


class DatesPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/dates/').func, pages.views.dates_page)

    def test_uses_about_template(self):
        response = self.client.get('/dates/')
        self.assertTemplateUsed(response, 'dates.html')


class CollegesPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/colleges/').func, pages.views.colleges_page)

    def test_uses_about_template(self):
        response = self.client.get('/colleges/')
        self.assertTemplateUsed(response, 'colleges.html')
