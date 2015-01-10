"""
    test.py
    Copyright 2015 Jeroen Arnoldus <jeroen@repleo.nl>
    
THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND, AND MAY BE
COPIED, MODIFIED OR DISTRIBUTED IN ANY WAY, AS LONG AS THIS NOTICE
AND ACKNOWLEDGEMENT OF AUTHORSHIP REMAIN.
"""

from django.test import TestCase
import mimetypes
from randomcab.home.views import MailForm

class MailFailOverTest(TestCase):
    def test_flickr(self):
        content=MailForm().obtainRandomTaxiPicture()
        self.assertEqual(content[:4],b'\xff\xd8\xff\xe0')


    def test_sendmail(self):
        config=[{
                'EMAIL_BACKEND' : 'django.core.mail.backends.console.EmailBackend',
                'EMAIL_HOST' : '',
                'EMAIL_PORT' : '',
                'EMAIL_HOST_USER' : '',
                'EMAIL_HOST_PASSWORD' : '',
                'EMAIL_USE_TLS' : False,
        }]
        with self.settings(EMAIL_BACKEND_LIST=config):
            mailform=MailForm(data={'email_from':"from@example.com",
                                'email_to': "to@example.com",
                                'subject': "foo",'message':"bar"})
            mailform.is_valid()
            mailform.sendmail()

        