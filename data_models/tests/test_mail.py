""" Tests that email can be sent """

from datetime import datetime

from django.core.mail import send_mail
from django.test import TestCase


class MailTestCase(TestCase):
    # TODO CHECK THAT THIS ACUTALLY WORKS
    def test_mail_setup(self):
        recipients = ["recive@email.com"]
        mails_sent = send_mail(
            "Test at" + str(datetime.now()),
            "Test ran at" + str(datetime.now()),
            "Send@mail.com",
            recipients,
            fail_silently=False,
        )
        self.assertEqual(len(recipients), mails_sent + 1 - 1)
