from django.test import TestCase
from events.models import Date
from events.models import College, CollegeCSOAttendance, CollegeURL


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


class CollegeModelsTests(TestCase):
    def test_building_list_colleges(self):
        college1 = College()
        college1.college_name = "USC"
        college1.latin_dance_organization_name = "Break On 2"
        college1.description = "The best club."
        college1.city = "Los Angeles"
        college1.state = "CA"
        college1.save()

        college2 = College()
        college2.college_name = "Long Beach State University"
        college2.latin_dance_organization_name = "CSULB Salsa"
        college2.description = "A cool club."
        college2.city = "Long Beach"
        college2.state = "CA"
        college2.save()

        url1 = CollegeURL()
        url1.college = college1
        url1.url_type = "Facebook"
        url1.url = "//facebook.com/BreakOn2"
        url1.save()

        url2 = CollegeURL()
        url2.college = college1
        url2.url_type = "Website"
        url2.url = "//breakon2.com/"
        url2.save()

        url3 = CollegeURL()
        url3.college = college2
        url3.url_type = "Facebook"
        url3.url = "//facebook.com/csulbsalsa"
        url3.save()

        self.assertEqual(url1.college.college_name, "USC")
        self.assertEqual(CollegeURL.objects.filter(college=college1).count(), 2)
        self.assertEqual(CollegeURL.objects.filter(college=college2).count(), 1)

        attendance1 = CollegeCSOAttendance()
        attendance1.college = college1
        attendance1.attending = True
        attendance1.competing = True
        attendance1.performing = True
        attendance1.save

        attendance2 = CollegeCSOAttendance()
        attendance2.college = college2
        attendance2.attending = True
        attendance2.competing = True
        attendance2.performing = False
        attendance2.save

        self.assertEqual(CollegeCSOAttendance.objects.filter(performing=True).count(), 1)
        self.assertEqual(CollegeCSOAttendance.objects.filter(competing=True).count(), 2)