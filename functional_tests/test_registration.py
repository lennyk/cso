import os
import sys

from django.core.exceptions import ImproperlyConfigured
from django.utils.http import urlencode
from selenium.webdriver.support.ui import Select

from .base import FunctionalTest
from cso.models import CSOUser


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

        # User sees a Registration link and clicks it
        self.click_link_assert_new_page('Registration')

        # User selects the Facebook option
        self.browser.find_element_by_css_selector('#login-buttons a.btn-facebook').click()

        # Selenium switches to the newest window
        self.switch_to_newest_window()

        # User logs in with Facebook
        self.browser.find_element_by_id('email').send_keys(email)
        self.browser.find_element_by_id('pass').send_keys(password)
        self.browser.find_element_by_css_selector('label#loginbutton > input[type="submit"]').click()

        # Selenium switches to the newest window
        self.switch_to_newest_window()

        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertTrue('Sign Up' in body_text)

    def register_new_login(self, dance_orientation='Lead'):
        Select(self.browser.find_element_by_id('id_partner_type')).select_by_visible_text(dance_orientation)
        self.browser.find_element_by_css_selector('form#signup_form button[type="submit"]').click()

    def logout(self):
        self.browser.find_element_by_link_text('Logout').click()
        self.assertNotIn('Logout', self.browser.find_element_by_id('cso-navbar').text)
        self.assertIn('You have signed out.', self.browser.find_element_by_tag_name('body').text)

    def logout_of_facebook(self, email):
        user = CSOUser.objects.filter(email=email)[0]
        social = user.social_auth.get(provider='facebook')
        parameters = {'access_token': social.extra_data['access_token'], 'confirm': 1, 'next': self.server_url}
        logout_url = "https://www.facebook.com/logout.php?{}".format(urlencode(parameters))
        self.browser.get(logout_url)

    def test_user_registration_and_login(self):
        # Richard logs in with Facebook
        self.login_with_facebook(FACEBOOK_EMAIL_RICHARD, FACEBOOK_PASSWORD_RICHARD)

        # Richard does not see an Event Management link
        links = self.browser.find_elements_by_name('a')
        self.assertNotIn('Event Management', links)

        # Richard completes his registration
        self.register_new_login()

        # Richard is on the Registration page
        self.assertIn('Registration Details', self.browser.find_element_by_tag_name('body').text)

        # Richard logs out
        self.logout()

        # Richard is on the homepage
        self.assertIn('The Collegiate Salsa Open', self.browser.find_element_by_tag_name('body').text)

        # TODO: either re-implement the admin link for staff or remove this commented out block
        # # Richard MAGICALLY becomes staff
        # richard = CSOUser.objects.filter(email=FACEBOOK_EMAIL_RICHARD)[0]
        # richard.is_staff = True
        # richard.save()
        #
        # # Richard logs in with Facebook
        # self.login_with_facebook(FACEBOOK_EMAIL_RICHARD, FACEBOOK_PASSWORD_RICHARD)
        #
        # # Richard clicks the Event Management link
        # self.browser.find_element_by_link_text('Event Management').click()
        #
        # # Richard sees the Event Management index
        # self.assertIn('Django administration', self.browser.title)
