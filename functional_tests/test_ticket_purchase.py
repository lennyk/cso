from datetime import date

from django.core import management

from .base import FunctionalTest


class TicketPurchase(FunctionalTest):
    def setUp(self):
        super().setUp()
        management.call_command('loaddata', 'fixtures/test/users/randy.json')
        management.call_command('loaddata', 'fixtures/test/users/bobby.json')
        management.call_command('loaddata', 'fixtures/test/college_ticket_presales_open.json')
        management.call_command('loaddata', 'fixtures/test/public_ticket_presales_open.json')

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

    def login_as_bobby(self):
        self.login_with_email(self.BOBBY_EMAIL, self.BOBBY_PASSWORD)

    def test_registered_user_can_purchase_ticket(self):
        # Randy sees a countdown showing tickets are available
        self.browser.get(self.server_url)
        self.assert_text_in_page('Tickets Remaining')

        # Randy logs in
        self.login_as_randy()

        # Randy sees a message indicating he does not have a ticket purchased and he can buy one
        self.assert_text_in_page('ticket sales are open!', case_insensitive=True)

        # Randy clicks the Purchase Ticket button and is brought to the ticket purchase page
        self.browser.find_element_by_link_text('Purchase Ticket').click()
        self.assert_text_in_page('Enter your credit card details.')

        # Randy puts in his deets
        self.browser.find_element_by_id('cc-name').send_keys(self.RANDY_FULL_NAME)
        self.browser.find_element_by_id('cc-number').send_keys('4242424242424242')
        self.browser.find_element_by_id('cc-exp').send_keys('01' + str(date.today().year + 1))
        self.browser.find_element_by_id('cc-cvc').send_keys('111')

        # Randy clicks the magic button
        with self.wait_for_page_load(self.browser):
            self.browser.find_element_by_css_selector('[type="submit"]').click()

        # Randy sees that he's purchased his ticket
        self.assert_text_in_page('Success! You\'ve purchased your ticket', case_insensitive=True)
        self.assert_text_in_page('You\'ve purchased your ticket! See you at the CSO!', case_insensitive=True)

    def test_nonSchoolAffiliated_cannotPurchaseTicket_whenPublicSalesClosed(self):
        management.call_command('loaddata', 'fixtures/test/public_ticket_presales_closed.json')

        # Bobby logs in
        self.login_as_bobby()

        # Bobby sees a message indicating he does not have a ticket purchased but he can't buy one yet
        self.assert_text_in_page('Public ticket sales are not open yet.', case_insensitive=True)

    def test_nonSchoolAffiliated_canPurchaseTicket_whenPublicSalesOpen(self):
        management.call_command('loaddata', 'fixtures/test/public_ticket_presales_open.json')

        # Bobby logs in
        self.login_as_bobby()

        # Randy sees a message indicating he does not have a ticket purchased and he can buy one
        self.assert_text_in_page('ticket sales are open!', case_insensitive=True)

        # Randy clicks the Purchase Ticket button and is brought to the ticket purchase page
        self.browser.find_element_by_link_text('Purchase Ticket').click()
        self.assert_text_in_page('Enter your credit card details.')