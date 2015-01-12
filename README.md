RandomCab - Send random cabs to your friends
==================================
https://www.randomcab.com

Problem
-------------
Create a service that accepts the necessary information and sends emails. It should provide an abstraction between two different email service providers. If one of the services goes down, your service can quickly failover to a different provider without affecting your customers.

Application
-------------
RandomCab is a simple service which allows someone to send an email message to a friend. This message is enriched by RandomCab with an awesome Taxi picture gathered from Flickr. RandomCab is failsafe, it uses multiple email providers. It automatically failover to a secondary email provider in case the primary one fails.

RandomCab is full stack application. It handles all the front-end and back-end needs for sending the mails.

Implementation
-------------
RandomCab is implemented in Django / Python3 which provides an MVC architecture implementation. To achieve the email provider failover a mail failover backend class plugin is added. This mail failover backed iterates over a list of email providers, and tries to send the emails starting at the first provider of the list. The used mail sending protocol is SMTP, as this protocol is most defacto standard to send emails and an SMTP server can easily be hosted. In case if it is necessary, the architecture allows to add special email backends for web-api providers.

RandomCab attaches a taxi picture to the email. Every time a RandomCab is sent, flickr is queried for its most interesting taxi pictures. RandomCab downloads a random picture of this list and attaches it to the email for it is sent to the receiver.

RandomCab's UI is a simple HTML one pager without AJAX. All the feedback is rendered using templates. Enabling AJAX would have made the application more complex than appropriate for its goal.

The configuration of the application is separated in an configuration file. This allows easy deploy in different environments, like development and test. In these cases only the configuration file differs. In production, errors (500) are mailed to system administration including a stack trace. This enables fast reporting of errors, and fast error fixing.

Testing
-------------
RandomCab comes with a set of unit test for the mail failover backend and main view handlers. Execute manage.py test to run them

Live example
-------------
Send a RandomCab: https://www.randomcab.com


