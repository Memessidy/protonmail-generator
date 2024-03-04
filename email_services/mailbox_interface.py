from email_services.email_services import services
from exceptions.possible_exceptions import NotAvailableDomainException, GettingVerificationCodeException


class EmailBox:
    def __init__(self):
        self.__gen = self.__domains_gen()
        self.__email_class = None
        self.__email_domain = None

        self.__time_to_sleep = 5
        self.__tries_count = 10

    def __domains_gen(self):
        for service in services:
            yield service.class_of_service, service.domain_name

    def get_another_domain(self):
        try:
            self.__email_class, self.__email_domain = next(self.__gen)
        except StopIteration:
            raise NotAvailableDomainException('No more email domains available')

    @property
    def email_class(self):
        return self.__email_class

    @property
    def email_domain(self):
        return self.__email_domain

    def get_verification_code(self, username):
        box = self.__email_class(mailbox=username, subject_name="Proton Verification Code",
                                 tries_to_stop=self.__tries_count, sleeping_time=self.__time_to_sleep)
        try:
            result = box.get_code_by_many_tries()
            return result
        except Exception as exc:
            raise GettingVerificationCodeException(f'Something went wrong! {exc}')
