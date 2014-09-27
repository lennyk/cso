from django.test import TestCase
from django.core.urlresolvers import resolve
import pages


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/').func, cso.views.home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'cso/home.html')


class AboutPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/about/').func, cso.views.thelda_page)

    def test_uses_about_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'cso/thelda.html')


class ConstitutionPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/about/constitution/').func, cso.views.constitution_page)

    def test_uses_about_template(self):
        response = self.client.get('/about/constitution/')
        self.assertTemplateUsed(response, 'cso/constitution.html')


class DatesPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/dates/').func, cso.views.dates_page)

    def test_uses_about_template(self):
        response = self.client.get('/dates/')
        self.assertTemplateUsed(response, 'cso/dates.html')


class CollegesPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/colleges/').func, cso.views.colleges_page)

    def test_uses_about_template(self):
        response = self.client.get('/colleges/')
        self.assertTemplateUsed(response, 'cso/colleges.html')
