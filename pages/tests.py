from django.test import TestCase
from django.core.urlresolvers import resolve
import pages
from pages.models import Date


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/').func, pages.views.home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class AboutPageTest(TestCase):

    def test_about_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve('/about/').func, pages.views.thecso_page)

    def test_uses_about_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'thecso.html')


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


class DateModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        # date 1
        date1 = Date()
        date1.title = 'Event 1'
        date1.date = '2014-01-01'
        date1.time = None
        date1.description = 'event #1'
        date1.information = 'this is an event.'
        date1.is_active = True
        date1.save()

        # date 2
        date2 = Date()
        date2.title = 'Event 2'
        date2.date = '2014-01-02'
        date2.time = '08:00:00'
        date2.description = 'event #2'
        date2.information = 'this is another event.'
        date2.is_active = False
        date2.save()

        dates = Date.objects.all()
        active_dates = Date.objects.filter(is_active=True)
        self.assertEqual(dates.count(), 2)
        self.assertEqual(active_dates.count(), 1)
        self.assertEqual(dates[0], date1)
        self.assertEqual(dates[1], date2)
        self.assertEqual(dates[0].title, 'Event 1')
        self.assertEqual(dates[1].title, 'Event 2')
        self.assertEqual(dates[0].time, None)
        self.assertEqual(str(dates[1].time), '08:00:00')
