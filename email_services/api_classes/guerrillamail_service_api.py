from __future__ import print_function
from __future__ import unicode_literals

from datetime import tzinfo, timedelta, datetime
from time import time, sleep
import json
import requests

ZERO = timedelta(0)
SESSION_TIMEOUT_SECONDS = 3600


class UTC(tzinfo):
    """UTC"""

    #
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = UTC()


class GuerrillaMailException(Exception):
    def __init__(self, message):
        self.message = message


def _transform_dict(original, key_map):
    result = {}
    for (new_key, (old_key, transform_fn)) in list(key_map.items()):
        try:
            result[new_key] = transform_fn(original[old_key])
        except KeyError:
            pass
    return result


class Mail:
    @classmethod
    def from_response(cls, response_data):
        identity = lambda x: x
        return Mail(**_transform_dict(response_data, {
            'guid': ('mail_id', identity),
            'subject': ('mail_subject', identity),
            'sender': ('mail_from', identity),
            'datetime': ('mail_timestamp', lambda x: datetime.utcfromtimestamp(int(x)).replace(tzinfo=utc)),
            'read': ('mail_read', int),
            'excerpt': ('mail_excerpt', identity),
            'body': ('mail_body', identity),
        }))

    def __init__(self, guid=None, subject=None, sender=None, datetime=None,
                 read=False, exerpt=None, excerpt=None, body=None):
        self.guid = guid
        self.subject = subject
        self.sender = sender
        self.datetime = datetime
        self.read = read
        self.exerpt = None
        self.excerpt = excerpt
        self.body = body

    @property
    def time(self):
        return self.datetime.time().replace(tzinfo=self.datetime.tzinfo) if self.datetime else None


class GuerrillaMailSession(object):

    def __init__(self, session_id=None, email_address=None, email_timestamp=0, **kwargs):
        self.client = GuerrillaMailClient(**kwargs)
        self.session_id = session_id
        self.email_timestamp = email_timestamp
        self.email_address = email_address

    def _update_session_state(self, response_data):
        try:
            self.session_id = response_data['sid_token']
        except KeyError:
            pass
        try:
            self.email_address = response_data['email_addr']
        except KeyError:
            pass
        try:
            self.email_timestamp = response_data['email_timestamp']
        except KeyError:
            pass

    def is_expired(self):
        current_time = int(time())
        expiry_time = self.email_timestamp + SESSION_TIMEOUT_SECONDS - 5
        return current_time >= expiry_time

    def _delegate_to_client(self, method_name, *args, **kwargs):
        client_method = getattr(self.client, method_name)
        response_data = client_method(session_id=self.session_id, *args, **kwargs)
        self._update_session_state(response_data)
        return response_data

    def get_session_state(self):
        self._ensure_valid_session(fully_populate=True)
        return {
            'email_address': self.email_address
        }

    def set_email_address(self, address_local_part):
        self._delegate_to_client('set_email_address', address_local_part=address_local_part)

    def _renew_session(self):
        if self.email_address:
            self.set_email_address(self.email_address)
        else:
            self._delegate_to_client('get_email_address')

    def _ensure_valid_session(self, fully_populate=False):
        if self.session_id is None or self.is_expired() or fully_populate and not self.email_address:
            self._renew_session()
        if self.session_id is None:
            raise GuerrillaMailException('Failed to obtain session id')

    def get_email_list(self, offset=0):
        self._ensure_valid_session()
        response_data = self._delegate_to_client('get_email_list', offset=offset)
        email_list = response_data.get('list')
        return [Mail.from_response(e) for e in email_list] if email_list else []

    def get_email(self, email_id):
        return Mail.from_response(self._delegate_to_client('get_email', email_id=email_id))


class GuerrillaMailClient:
    def __init__(self, base_url='http://api.guerrillamail.com', client_ip='127.0.0.1'):
        self.base_url = base_url
        self.client_ip = client_ip

    def _do_request(self, session_id, **kwargs):
        url = self.base_url + '/ajax.php'
        kwargs['ip'] = self.client_ip
        if session_id is not None:
            kwargs['sid_token'] = session_id
        response = requests.get(url, params=kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise GuerrillaMailException(('Request failed: {e.request.url} ' +
                                          '{e.response.status_code} {e.response.reason}').format(e=e))
        data = json.loads(response.text)
        return data

    def get_email_address(self, session_id=None):
        return self._do_request(session_id, f='get_email_address')

    def get_email_list(self, session_id, offset=0):
        if session_id is None:
            raise ValueError('session_id is None')
        return self._do_request(session_id, f='get_email_list', offset=offset)

    def get_email(self, email_id, session_id=None):
        response_data = self._do_request(session_id, f='fetch_email', email_id=email_id)
        if not response_data:
            raise GuerrillaMailException('Not found: ' + str(email_id))
        return response_data

    def set_email_address(self, address_local_part, session_id=None):
        return self._do_request(session_id, f='set_email_user', email_user=address_local_part)


class GuerrillaMail:
    def __init__(self, mailbox, subject_name, tries_to_stop, sleeping_time):
        self.subject_name = ""
        self.sleeping_time = sleeping_time
        self.session = GuerrillaMailSession(email_address=mailbox)
        self.content = None
        self.tries_count = tries_to_stop

    def get_code_by_many_tries(self):
        content = None
        for _ in range(self.tries_count):
            for mail in self.session.get_email_list():
                if 'guerrilla' not in mail.sender:
                    content = self.session.get_email(mail.guid).body
                if content:
                    return content.split('<br>')[1].strip('</p>')
                else:
                    sleep(self.sleeping_time)
        else:
            return None
