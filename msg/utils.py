from datetime import datetime

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from msg.models import BirthdayEmailSent


def employees_api_call():
    url = 'https://interview-assessment-1.realmdigital.co.za/employees/'
    call = requests.get(url).json()
    return call


def exclude_api_call():
    url = 'https://interview-assessment-1.realmdigital.co.za/do-not-send-birthday-wishes/'
    call = requests.get(url).json()
    return call


def parse_api_for_exlusions(api_data, exclusions):
    today = datetime.today().date()
    sending_list = []
    for emp in api_data:
        if emp.get('employmentStartDate') and not emp['employmentEndDate']:
            # person has started and is still employed.
            if emp['id'] not in exclusions:
                # checks if they are not excluded
                birth = datetime.strptime(emp['dateOfBirth'], '%Y-%m-%dT%H:%M:%S').date()
                if birth.day == today.day and birth.month == today.month:
                    age = today.year - birth.year
                    sending_dict = {
                        'first_name': emp['name'],
                        'last name': emp['lastname'],
                        'email': f'{emp["name"]}.{emp["lastname"]}@testcompany.com',
                        'age': age,
                    }
                    sending_list.append(sending_dict)
        elif emp.get('employmentStartDate') and emp['employmentEndDate']:
            # person has started but has an employment end date
            end_date = datetime.strptime(emp['employmentEndDate'], '%Y-%m-%dT%H:%M:%S')
            if end_date < today:
                # checks whether end date is after today
                if emp['id'] not in exclusions:
                    # checks if they are not excluded
                    ##TODO: Work on leap year
                    birth = datetime.strptime(emp['dateOfBirth'], '%Y-%m-%dT%H:%M:%S').date()
                    if birth.day == today.day and birth.month == today.month:
                        age = today.year - birth.year
                        sending_dict = {
                            'first_name': emp['name'],
                            'last name': emp['lastname'],
                            'email': f'{emp["name"]}.{emp["lastname"]}@testcompany.com',
                            'age': age,
                        }
                        sending_list.append(sending_dict)

    return sending_list


def send_birthday_email(sending_list):
    subject = 'Happy Birthday'
    from_email = settings.EMAIL_HOST_USER
    today = datetime.today()
    birthday_sent_model = BirthdayEmailSent
    sent_query = birthday_sent_model.objects.filter(date=today)
    with open(str(settings.BASE_DIR) + '/templates/happy_birthday.txt') as file:
        birthday_message = file.read()
    for sending in sending_list:
        msg_check = sent_query.filter(recipient=sending['email'])
        if not msg_check:
            to_email = [sending['email']]
            message = EmailMultiAlternatives(subject=subject, body=birthday_message, from_email=from_email, to=to_email)
            html_template = get_template('happy_birthday.html').render(context={'name': sending['first_name']})
            message.attach_alternative(html_template, 'text/html')
            message.send()
            check = birthday_sent_model.objects.create(recipient=sending['email'], date=today, message_sent=True)
            check.save()
        elif msg_check.get(recipient=sending['email']).message_sent == 'False':
            to_email = [sending['email']]
            message = EmailMultiAlternatives(subject=subject, body=birthday_message, from_email=from_email, to=to_email)
            html_template = get_template('happy_birthday.html').render(context={'name': sending['first_name']})
            message.attach_alternative(html_template, 'text/html')
            message.send()
            check = msg_check.get(recipient=sending['email'])
            check.message_sent = True
            check.save()

    return 'Birthday Messages Sent'


def happy_birthday():
    api_data = employees_api_call()
    exclusions = exclude_api_call()
    birthdays = parse_api_for_exlusions(api_data, exclusions)
    send_msg = send_birthday_email(birthdays)

    return send_msg

# TODO:Additional Message Functionalities for other use cases
# TODO: Write tests for all functions
