"""
    mail.py
    Copyright 2015 Jeroen Arnoldus <jeroen@repleo.nl>
    
THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND, AND MAY BE
COPIED, MODIFIED OR DISTRIBUTED IN ANY WAY, AS LONG AS THIS NOTICE
AND ACKNOWLEDGEMENT OF AUTHORSHIP REMAIN.

2015-01-10
  -Implements Mail Backend Failover system for Django. 
  
USAGE:
The failover system accepts a list of SMTP servers. When sending mails
it first tries to send the mails using the first server, if it fails it
tries the next one, etcetera. If no server is able to send the mail it
will generate an exception.
   
Example settings of SMTPs servers in settings.py:

EMAIL_BACKEND = "<PROJECTNAME>.backends.mail.MailFailOverBackend"
EMAIL_BACKEND_LIST = [
        {
            'EMAIL_BACKEND' : '<PROJECTNAME>.backends.mail.SSLEmailBackend',
            'EMAIL_HOST' : 'email-smtp.us-west-2.amazonaws.com',
            'EMAIL_PORT' : 465,
            'EMAIL_HOST_USER' : '',
            'EMAIL_HOST_PASSWORD' : '',
            'EMAIL_USE_TLS' : False,
        },
        {
            'EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
            'EMAIL_HOST' : 'smtp.sendgrid.net',
            'EMAIL_PORT' : 587,
            'EMAIL_HOST_USER' : '',
            'EMAIL_HOST_PASSWORD' : '',
            'EMAIL_USE_TLS' : True,
        },
        {
            'EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
            'EMAIL_HOST' : 'localhost',
            'EMAIL_PORT' : 25,
            'EMAIL_HOST_USER' : '',
            'EMAIL_HOST_PASSWORD' : '',
            'EMAIL_USE_TLS' : False,
        }
]

"""

__author__ = "Jeroen Arnoldus <jeroen@repleo.nl>"
__version__ = "$Rev$"
__date__ = "$Date$"
__copyright__ = "Copyright: 2015 Jeroen Arnoldus;"

from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail import get_connection

def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError

class MailFailOverBackend(BaseEmailBackend):

     
    def send_messages(self, email_messages):
        num_sent = 0;
        for service in getattr(settings, "EMAIL_BACKEND_LIST", []):
            try:
                backend = get_connection(service['EMAIL_BACKEND'],\
                                         host=service['EMAIL_HOST'],\
                                         port=service['EMAIL_PORT'],\
                                         username=service['EMAIL_HOST_USER'],\
                                         password=service['EMAIL_HOST_PASSWORD'],\
                                         use_tls=str_to_bool(str(service['EMAIL_USE_TLS'])))
                num_sent = backend.send_messages(email_messages)
                if num_sent >= len(email_messages):
                    break
            except:
                pass
        if num_sent < len(email_messages):
            raise Exception("Could not send all messages, please check SMTP services");        
        return num_sent


import smtplib
from django.core.mail.utils import DNS_NAME
from django.core.mail.backends.smtp import EmailBackend

class SSLEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = smtplib.SMTP_SSL(self.host, self.port,
                                           local_hostname=DNS_NAME.get_fqdn())
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise

