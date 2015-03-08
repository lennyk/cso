from django.core import management

from .base import FunctionalTest


class TicketPurchase(FunctionalTest):

    RANDY_EMAIL = 'randy@example.com'
    RANDY_EDU_EMAIL = 'randy@example.edu'
    RANDY_PASSWORD = 'password'

    def setUp(self):
        super().setUp()
        management.call_command('loaddata', 'fixtures/test/users/randy.json')
        management.call_command('loaddata', 'fixtures/test/college_ticket_presales_open.json')

    def login_with_email(self, email, password):
        # User goes to the CSO homepage
        self.browser.get(self.server_url)

        # User sees a Registration link and clicks it
        self.click_link_assert_new_page('Registration')

        # User clicks the login with email toggle radio button
        self.browser.find_element_by_id('email_login_select').click()

        # User logs in with email and password
        self.browser.find_element_by_id('id_login').send_keys(email)
        self.browser.find_element_by_id('id_password').send_keys(password)
        self.browser.find_element_by_id('email_login_button').click()

        # User is now on the Registration page
        self.assert_text_in_page('Registration Details')

    def login_as_randy(self):
        self.login_with_email(self.RANDY_EMAIL, self.RANDY_PASSWORD)

    def test_login_with_email(self):

        # Randy goes to the CSO homepage
        self.browser.get(self.server_url)

        # Randy sees a Registration link and clicks it
        self.click_link_assert_new_page('Registration')

        signup_button = self.browser.find_element_by_id('email_signup_button')
        login_button = self.browser.find_element_by_id('email_login_button')

        # Randy sees a Sign Up with email button but doesn't see a Login with email button
        self.assertTrue(signup_button.is_displayed())
        self.assertFalse(login_button.is_displayed())

        # Randy clicks the login with email toggle radio button
        self.browser.find_element_by_id('email_login_select').click()

        # Randy sees the Sign Up with email button has gone away and the Login with email button is visible
        self.assertFalse(signup_button.is_displayed())
        self.assertTrue(login_button.is_displayed())

        # Randy inputs his email and password
        self.browser.find_element_by_id('id_login').send_keys(self.RANDY_EMAIL)
        self.browser.find_element_by_id('id_password').send_keys(self.RANDY_PASSWORD)

        # Randy submits the form and and he is now on the Registration page
        self.browser.find_element_by_id('email_login_button').click()
        self.assert_text_in_page('Registration Details')

    def test_registered_user_can_purchase_ticket(self):
        # Randy logs in
        self.login_as_randy()

        # Randy sees a message indicating he does not have a ticket purchased and he can buy one
        self.assert_text_in_page('ticket sales are open! purchase one by clicking purchase ticket below', case_insensitive=True)
