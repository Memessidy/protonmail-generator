from collections import namedtuple
from .api_classes.guerrillamail_service_api import GuerrillaMail
from .api_classes.maildrop_service_api import MailDrop

Service = namedtuple('Service', 'name_of_service class_of_service domain_name')

services = [Service('maildrop', MailDrop, '@maildrop.cc'),
            Service('guerrillamail', GuerrillaMail, '@guerrillamail.com')]
