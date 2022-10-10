from datetime import datetime

from django.test import TestCase

from mail.models import EmailSent
from mail.utils import send_email_message


# Create your tests here.
class ModelTest(TestCase):

    def testEmailSent(self):
        sent_mail = EmailSent.objects.create(
            recipient='test@email.com',
            message_sent=True,
            topic='A random topic',
            date=datetime.today()
        )
        self.assertEqual(str(sent_mail), 'A random topic: test@email.com')
        self.assertTrue(isinstance(sent_mail, EmailSent))

    def test_send_email_message(self):
        send = send_email_message(
            'random subject',
            [{
                'first_name': 'Test',
                'last_name': 'Man',
                'email': ['test.man@testing.com', ],
                'age': 21,
                'topic': 'random topic'
            }, ]
        )

        self.assertEqual(send, 'Emails have been sent')
