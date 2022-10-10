from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

from mail.models import EmailSent


def send_email_message(subject, sending_list):
    """ sending an email to a list of users with context in each list item."""
    from_email = settings.EMAIL_HOST_USER
    today = datetime.today()
    sent_qs = EmailSent
    sent_today_query = sent_qs.objects.filter(date=today)
    # For loop through sending list comes here
    for sending in sending_list:
        msg_check = sent_today_query.filter(recipient=sending['email'], topic=sending['topic'])
        if not msg_check:
            message = get_template('context_email.html').render(context=sending)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=sending['email'],
            )
            mail.content_subtype = 'html'
            mail.send()
            sent_qs.objects.create(
                recipient=sending['email'],
                topic=sending['topic'],
                date=today,
                message_sent=True
            )
        elif msg_check.get(recipient=sending['email'], topic=sending['topic']).message_sent == 'False':
            message = get_template('context_email.html').render(context=sending)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=sending['email'],
            )
            mail.content_subtype = 'html'
            mail.send()
            check = msg_check.get(recipient=sending['email'], topic=sending['topic'])
            check.message_sent = True
            check.save()

    return 'Emails have been sent'
