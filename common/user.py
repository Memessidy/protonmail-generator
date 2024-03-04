from email_services.mailbox_interface import EmailBox
from reg_values_generators.generators import return_user_data


class User:
    def __init__(self):
        self.email_interface = EmailBox()

        self.__nickname = None
        self.__password = None

    def generate_new_user(self):
        self.__nickname, self.__password = return_user_data()

    def get_another_domain(self):
        self.email_interface.get_another_domain()

    @property
    def nickname(self):
        return self.__nickname

    @property
    def password(self):
        return self.__password

    @property
    def full_email_name_for_verification(self):
        return self.nickname + self.email_interface.email_domain

    @property
    def verification_code(self):
        return self.email_interface.get_verification_code(self.nickname)
