from exceptions.possible_exceptions import NoEmailVerification, GettingVerificationCodeException
from pom_objects.base_playwright import BasePlaywright
from common.user import User
import time
import datetime
import settings


class ProtonmailCreationPages(BasePlaywright):
    def __init__(self):
        super().__init__()
        self.url = settings.protonmail_registration_address
        self.protonmail_domain = settings.protonmail_domain
        self.user = User()

    # def change_language_to_eng_button(self):
    #     print("Changing language to eng on proton page")
    #     self.page.get_by_test_id("dropdown-button").click()
    #     self.page.get_by_role("button", name="English").click()

    def set_user_data(self):
        print("Filling out the fields on the registration page")
        (self.page.frame_locator("iframe[title=\"Username\"]")
         .get_by_test_id("input-input-element").fill(self.user.nickname))
        self.page.get_by_label("Password", exact=True).fill(self.user.password)
        self.page.get_by_label("Repeat password").fill(self.user.password)

    def create_account_button_click(self):
        print("Creating account button pressed")
        self.page.get_by_role("button", name="Create account").click()

    def switch_temporary_email(self):
        self.user.get_another_domain()
        print(f"New domain is {self.user.email_interface.email_domain}")

    def try_register_using_temp_mail(self):
        print("Finding email button and field...")
        try:
            self.page.get_by_test_id("tab-header-email-button").click()
        except:
            pass

        try:
            self.page.get_by_test_id("input-input-element").fill(self.user.full_email_name_for_verification)
        except Exception:
            raise NoEmailVerification('Verification by email is not available now! Please try again later or use vpn.')

        self.page.get_by_role("button", name="Get verification code").click()
        alert = self.page.get_by_role('alert').inner_text()
        return alert

    def register_with_temporary_email(self):
        print("Trying to register using temporary email")
        alert = self.try_register_using_temp_mail()
        if 'Please wait a few minutes' in alert:
            time.sleep(10)
            self.page.get_by_role("button", name="Get verification code").click()
        else:
            while ('Email address verification temporarily disabled for this email domain. '
                   'Please try another verification method') in alert:
                print(f"Email domain {self.user.email_interface.email_domain} is not enable for verification now!")
                self.switch_temporary_email()
                alert = self.try_register_using_temp_mail()

    def insert_verification_code(self):
        while True:
            print("Trying to find a verification code")
            try:
                code = self.user.verification_code
                if code:
                    print(f"Verification code: {code}")
                    break
            except GettingVerificationCodeException:
                print(f'{self.user.email_interface.email_domain} domain is not working now...')
                self.switch_temporary_email()
                self.page.get_by_role("button", name="Back").click()
                self.register_with_temporary_email()

        self.page.get_by_test_id("input-input-element").fill(code)
        self.page.get_by_role("button", name="Verify").click()

    def finishing_registration(self):
        print("Finishing registration...")
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_role("button", name="Maybe later").click()
        self.page.get_by_role("button", name="Confirm").click()

        # self.page.wait_for_load_state('networkidle')
        # try:
        #     self.page.get_by_role("button", name="Next", exact=True).click()
        #     self.page.get_by_role("button", name="Next", exact=True).click()
        #     self.page.get_by_role("button", name="Skip").click()
        # except:
        #     print('Account created, but advertising is not skipped')

    def run_registration(self):
        self.go_to(self.url)
        # self.change_language_to_eng_button()
        self.set_user_data()
        self.create_account_button_click()
        self.register_with_temporary_email()
        self.insert_verification_code()
        self.finishing_registration()

    def create_accounts(self, count: int):
        self.user.get_another_domain()
        try:
            for i in range(1, count + 1):
                if i > 1:
                    print(f"Waiting {settings.time_to_sleep_before_run_next} seconds before starting next...")
                    time.sleep(settings.time_to_sleep_before_run_next)
                print(f"Creating {i} account")
                self.user.generate_new_user()
                self.run_registration()
                protonmail_login, protonmail_password = self.user.nickname + self.protonmail_domain, self.user.password
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield protonmail_login, protonmail_password, current_time

        except Exception as exc:
            raise Exception(exc)
        finally:
            self.close_session()
