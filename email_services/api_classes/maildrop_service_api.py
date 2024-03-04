import requests
import re
import time


class MailDrop:
    def __init__(self, mailbox, subject_name, tries_to_stop, sleeping_time):
        self.__mailbox = mailbox
        self.__subject_name = subject_name
        self.__headers = {'content-type': 'application/json', }
        self.__base_url = 'https://api.maildrop.cc/graphql'
        self.__message_id = None
        self.__content_html = None
        self.__verification_code = None
        self.__tries_to_stop = tries_to_stop
        self.__sleeping_time = sleeping_time

    def __get_message_id(self):
        json_data = {'query': 'query Example { inbox(mailbox:"%s") { id headerfrom subject date } }' % self.__mailbox}
        response = requests.post(self.__base_url, headers=self.__headers, json=json_data)
        all_data = response.json()['data']['inbox']
        if not all_data:
            return False
        cur_message = None

        for message in all_data:
            subject = message['subject']
            if subject == self.__subject_name:
                cur_message = message
        if not cur_message:
            return False
        self.__message_id = cur_message['id']
        return True

    def __get_content(self):
        json_data = {'query': 'query Example {\n  message(mailbox:"%s", id:"%s") '
                              '{ id headerfrom subject date html }\n}' % (self.__mailbox, self.__message_id)}
        response = requests.post('https://api.maildrop.cc/graphql', headers=self.__headers, json=json_data)
        self.__content_html = response.json()['data']['message']['html']

    def __get_verification_code(self):
        self.__verification_code = re.search(r'\d{4,10}', self.__content_html).group()

    def get_code(self):
        message_exists = self.__get_message_id()
        if message_exists:
            self.__get_content()
            self.__get_verification_code()
            return self.__verification_code

    def get_code_by_many_tries(self):
        verification_code = None
        tries = 0

        while not verification_code:
            if tries >= self.__tries_to_stop:
                return None
            else:
                verification_code = self.get_code()
                tries += 1
                if not verification_code:
                    time.sleep(self.__sleeping_time)
        return verification_code
