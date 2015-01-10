"""
    test.py
    Copyright 2015 Jeroen Arnoldus <jeroen@repleo.nl>
    
THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND, AND MAY BE
COPIED, MODIFIED OR DISTRIBUTED IN ANY WAY, AS LONG AS THIS NOTICE
AND ACKNOWLEDGEMENT OF AUTHORSHIP REMAIN.
"""

from django.test import TestCase
from randomcab.backends import mail
from django.core.mail import EmailMessage

class MailFailOverTest(TestCase):
    def runMailFailOverBackendWithConfig(self,config):
        with self.settings(EMAIL_BACKEND_LIST=config):
            backend=mail.MailFailOverBackend();
            email_message=EmailMessage("foo", "body", "from@example.com",
                    ["to@example.com"], ["bcc@example.com"])
            return backend.send_messages([email_message])

    def test_no_mailserver(self):
        with self.assertRaises(Exception):
            self.runMailFailOverBackendWithConfig([])

    def test_one_ok_mailserver(self):
        config=[{
                'EMAIL_BACKEND' : 'django.core.mail.backends.dummy.EmailBackend',
                'EMAIL_HOST' : '',
                'EMAIL_PORT' : '',
                'EMAIL_HOST_USER' : '',
                'EMAIL_HOST_PASSWORD' : '',
                'EMAIL_USE_TLS' : False,
        }]
        result=self.runMailFailOverBackendWithConfig(config)
        self.assertEqual(result, 1)
            
    def test_two_ok_mailserver(self):
        config=[{
                'EMAIL_BACKEND' : 'django.core.mail.backends.dummy.EmailBackend',
                'EMAIL_HOST' : '',
                'EMAIL_PORT' : '',
                'EMAIL_HOST_USER' : '',
                'EMAIL_HOST_PASSWORD' : '',
                'EMAIL_USE_TLS' : False,
        },
        {
                'EMAIL_BACKEND' : 'django.core.mail.backends.dummy.EmailBackend',
                'EMAIL_HOST' : '',
                'EMAIL_PORT' : '',
                'EMAIL_HOST_USER' : '',
                'EMAIL_HOST_PASSWORD' : '',
                'EMAIL_USE_TLS' : False,
        }
        ]
        result=self.runMailFailOverBackendWithConfig(config)
        self.assertEqual(result, 1)

    def test_two_failover_mailserver(self):
        config=[{
            '    EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
                'EMAIL_HOST' : 'smtp.sendgrid.net',
                'EMAIL_PORT' : 587,
                'EMAIL_HOST_USER' : 'foo',
                'EMAIL_HOST_PASSWORD' : 'bar',
                'EMAIL_USE_TLS' : True,
        },
        {
                'EMAIL_BACKEND' : 'django.core.mail.backends.dummy.EmailBackend',
                'EMAIL_HOST' : '',
                'EMAIL_PORT' : '',
                'EMAIL_HOST_USER' : '',
                'EMAIL_HOST_PASSWORD' : '',
                'EMAIL_USE_TLS' : False,
        }
        ]
        result=self.runMailFailOverBackendWithConfig(config)
        self.assertEqual(result, 1)
        
    def test_one_fail_mailserver(self):
        with self.assertRaises(Exception):
            config=[{
                '    EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
                    'EMAIL_HOST' : 'smtp.sendgrid.net',
                    'EMAIL_PORT' : 587,
                    'EMAIL_HOST_USER' : 'foo',
                    'EMAIL_HOST_PASSWORD' : 'bar',
                    'EMAIL_USE_TLS' : True,
            }
            ]
            result=self.runMailFailOverBackendWithConfig(config)
            self.assertEqual(result, 1)

    def test_two_fail_mailserver(self):
        with self.assertRaises(Exception):
            config=[{
                '    EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
                    'EMAIL_HOST' : 'smtp.sendgrid.net',
                    'EMAIL_PORT' : 587,
                    'EMAIL_HOST_USER' : 'foo',
                    'EMAIL_HOST_PASSWORD' : 'bar',
                    'EMAIL_USE_TLS' : True,
            },
            {
                    'EMAIL_BACKEND' : '<PROJECTNAME>.backends.mail.SSLEmailBackend',
                    'EMAIL_HOST' : 'email-smtp.us-west-2.amazonaws.com',
                    'EMAIL_PORT' : 465,
                    'EMAIL_HOST_USER' : 'foo',
                    'EMAIL_HOST_PASSWORD' : 'bar',
                    'EMAIL_USE_TLS' : False,
            }
            ]
            result=self.runMailFailOverBackendWithConfig(config)
            self.assertEqual(result, 1)
            
    def test_three_failover_mailserver(self):
        config=[{
            '    EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
                'EMAIL_HOST' : 'smtp.sendgrid.net',
                'EMAIL_PORT' : 587,
                'EMAIL_HOST_USER' : 'foo',
                'EMAIL_HOST_PASSWORD' : 'bar',
                'EMAIL_USE_TLS' : True,
        },
        {
                'EMAIL_BACKEND' : '<PROJECTNAME>.backends.mail.SSLEmailBackend',
                'EMAIL_HOST' : 'email-smtp.us-west-2.amazonaws.com',
                'EMAIL_PORT' : 465,
                'EMAIL_HOST_USER' : 'foo',
                'EMAIL_HOST_PASSWORD' : 'bar',
                'EMAIL_USE_TLS' : False,
        },
        {
                'EMAIL_BACKEND' : 'django.core.mail.backends.dummy.EmailBackend',
                'EMAIL_HOST' : '',
                'EMAIL_PORT' : '',
                'EMAIL_HOST_USER' : '',
                'EMAIL_HOST_PASSWORD' : '',
                'EMAIL_USE_TLS' : False,
        }
        ]
        result=self.runMailFailOverBackendWithConfig(config)
        self.assertEqual(result, 1)
            