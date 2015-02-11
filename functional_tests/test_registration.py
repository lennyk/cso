from django.core.exceptions import ImproperlyConfigured
from .base import FunctionalTest
from django.contrib.auth.models import User
from django.utils.http import urlencode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import sys
from unittest import skip

if os.getenv('DJANGO_CONFIGURATION') == 'Live' or any('liveserver=cso.dance' in arg for arg in sys.argv):
    FACEBOOK_EMAIL_RICHARD = 'efrujdt_alisonsen_1410143138@tfbnw.net'
    FACEBOOK_PASSWORD_RICHARD = 'HkAyTG9oi6XWii'
    FACEBOOK_NAME_FIRST_RICHARD = 'Richard'
    FACEBOOK_EMAIL_JAMES = 'pgtlnhq_qinstein_1410143134@tfbnw.net'
    FACEBOOK_PASSWORD_JAMES = 'Dcwg96XAiwZyPq'
    FACEBOOK_NAME_FIRST_JAMES = 'James'
elif os.getenv('DJANGO_CONFIGURATION') == 'Sandbox' or any('liveserver=sandbox.cso.dance' in arg for arg in sys.argv):
    FACEBOOK_EMAIL_RICHARD = 'temhdjd_okelolasen_1410208049@tfbnw.net'
    FACEBOOK_PASSWORD_RICHARD = 'HkAyTG9oi6XWii'
    FACEBOOK_NAME_FIRST_RICHARD = 'Will'
    FACEBOOK_EMAIL_JAMES = 'rpitute_mcdonaldstein_1410208046@tfbnw.net'
    FACEBOOK_PASSWORD_JAMES = 'Dcwg96XAiwZyPq'
    FACEBOOK_NAME_FIRST_JAMES = 'Betty'
elif os.getenv('DJANGO_CONFIGURATION') == 'Dev':
    FACEBOOK_EMAIL_RICHARD = 'dkxdaoe_seligsteinwitz_1410208365@tfbnw.net'
    FACEBOOK_PASSWORD_RICHARD = 'HkAyTG9oi6XWii'
    FACEBOOK_NAME_FIRST_RICHARD = 'Will'
    FACEBOOK_EMAIL_JAMES = 'qjtdvjj_baosen_1410208361@tfbnw.net'
    FACEBOOK_PASSWORD_JAMES = 'Dcwg96XAiwZyPq'
    FACEBOOK_NAME_FIRST_JAMES = 'Barbara'
else:
    raise ImproperlyConfigured(
        'You must properly configure the DJANGO_CONFIGURATION envvar. Value: "{}"'.format(os.getenv('DJANGO_CONFIGURATION')))

SUPERUSER_TEST_NAME = 'fernando-YCWiGnRd9tE8tj'
SUPERUSER_TEST_PASSWORD = 'djJits6uT9vYvL'
# User.objects.create_superuser(SUPERUSER_TEST_NAME, '', SUPERUSER_TEST_PASSWORD)
# User.objects.filter(username=SUPERUSER_TEST_NAME).delete()


class HomePageUp(FunctionalTest):

    def login_with_facebook(self, email, password):
        # User goes to the CSO homepage
        self.browser.get(self.server_url)

        # User sees a login link and clicks it
        self.click_link_assert_new_page('Login')

        # User sees a login popup open
        self.see_login_popup_open()

        # User selects the Facebook option
        self.browser.find_element_by_css_selector('#loginModal a.btn-facebook').click()

        # User logs in with Facebook
        self.browser.find_element_by_id('email').send_keys(email)
        self.browser.find_element_by_id('pass').send_keys(password)
        self.browser.find_element_by_css_selector('label#loginbutton > input[type="submit"]').click()

        # User is on registration portal
        # TODO: check for registration panel

    def logout(self, name):
        self.browser.find_element_by_partial_link_text(name).click()
        # TODO: unify "Logout" / "Log out"
        self.browser.find_element_by_xpath('//a[text()="Logout"] | //a[text()="Log out"]').click()

    def logout_of_facebook(self, email):
        user = User.objects.filter(email=email)[0]
        social = user.social_auth.get(provider='facebook')
        parameters = {'access_token': social.extra_data['access_token'], 'confirm': 1, 'next': self.server_url}
        logout_url = "https://www.facebook.com/logout.php?{}".format(urlencode(parameters))
        self.browser.get(logout_url)

    def see_login_popup_open(self):
        WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.ID, 'loginModal')))
        login_popup_header = self.browser.find_element_by_css_selector('#loginModalLabel').text
        self.assertIn('Login', login_popup_header)

    def test_event_management_login_functionality(self):
        # Richard logs in with Facebook
        self.login_with_facebook(FACEBOOK_EMAIL_RICHARD, FACEBOOK_PASSWORD_RICHARD)

        # Richard does not see an Event Management link
        links = self.browser.find_elements_by_name('a')
        self.assertNotIn('Event Management', links)

        # Richard logs out
        self.browser.find_element_by_link_text(FACEBOOK_NAME_FIRST_RICHARD).click()
        self.browser.find_element_by_link_text('Logout').click()

        # Richard logs out of Facebook
        self.logout_of_facebook(FACEBOOK_EMAIL_RICHARD)

        # Richard is on the homepage
        self.assertIn('The CSO', self.browser.find_element_by_tag_name('body').text)

        # Richard MAGICALLY becomes staff
        richard = User.objects.filter(email=FACEBOOK_EMAIL_RICHARD)[0]
        richard.is_staff = True
        richard.save()

        # Richard logs in with Facebook
        self.login_with_facebook(FACEBOOK_EMAIL_RICHARD, FACEBOOK_PASSWORD_RICHARD)

        # Richard clicks the Event Management link
        self.browser.find_element_by_link_text('Event Management').click()

        # Richard sees the Event Management index
        self.assertIn('Django administration', self.browser.title)

        # Richard logs out
        self.logout(FACEBOOK_NAME_FIRST_RICHARD)
        # TODO: test this goes directly to the homepage, not the admin logout page

        # Richard logs out of Facebook
        self.logout_of_facebook(FACEBOOK_EMAIL_RICHARD)
