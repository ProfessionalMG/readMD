from datetime import datetime

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from mail.utils import send_email_message
from msg.models import BirthdayEmailSent


def employees_api_call():
    """"Gets List of Employees from API"""
    url = 'https://interview-assessment-1.realmdigital.co.za/employees/'
    call = requests.get(url)
    if call.status_code == 200:
        return call
    else:
        raise Exception(f'API Error, status code:{call.status_code}')


def exclude_api_call():
    """"Get a List of Exclusions"""
    url = 'https://interview-assessment-1.realmdigital.co.za/do-not-send-birthday-wishes/'
    call = requests.get(url)
    if call.status_code == 200:
        return call.json()
    else:
        raise Exception(f'API Error, status code:{call.status_code}')


def check_leap_year(year):
    if ((year % 400 == 0) or
            (year % 100 != 0) and
            (year % 4 == 0)):
        return True
    else:
        return False


def parse_api_for_exlusions(api_data, exclusions):
    """" Parse through all the employees with a valid employment start date. Check if end date is in the future and
    check for whether they are excluded. If they meet all requirements then their details are added to a context
    object which is then added to a list of emails to be sent """
    today = datetime.today().date()
    sending_list = []
    for emp in api_data.json():
        if emp.get('employmentStartDate') and not emp['employmentEndDate']:
            # person has started and is still employed.
            if emp['id'] not in exclusions:
                # checks if they are not excluded
                birth = datetime.strptime(emp['dateOfBirth'], '%Y-%m-%dT%H:%M:%S').date()
                if not check_leap_year(birth.year):
                    if birth.day == today.day and birth.month == today.month:
                        age = today.year - birth.year
                        sending_dict = {
                            'first_name': emp['name'],
                            'last name': emp['lastname'],
                            'email': f'{emp["name"]}.{emp["lastname"]}@testcompany.com',
                            'age': age,
                            'topic': 'birthday'
                        }
                        sending_list.append(sending_dict)
                elif not birth.month == 'February':
                    if birth.day == today.day and birth.month == today.month:
                        age = today.year - birth.year
                        sending_dict = {
                            'first_name': emp['name'],
                            'last name': emp['lastname'],
                            'email': f'{emp["name"]}.{emp["lastname"]}@testcompany.com',
                            'age': age,
                            'topic': 'birthday'
                        }
                        sending_list.append(sending_dict)
                elif not birth.day == 29:
                    if birth.day == today.day and birth.month == today.month:
                        age = today.year - birth.year
                        sending_dict = {
                            'first_name': emp['name'],
                            'last name': emp['lastname'],
                            'email': f'{emp["name"]}.{emp["lastname"]}@testcompany.com',
                            'age': age,
                            'topic': 'birthday'
                        }
                        sending_list.append(sending_dict)
                elif check_leap_year(today.year):
                    if birth.day == today.day and birth.month == today.month:
                        age = today.year - birth.year
                        sending_dict = {
                            'first_name': emp['name'],
                            'last name': emp['lastname'],
                            'email': f'{emp["name"]}.{emp["lastname"]}@testcompany.com',
                            'age': age,
                            'topic': 'birthday'
                        }
                        sending_list.append(sending_dict)
                else:
                    if birth.month == today.month and today.day == 28:
                        age = today.year - birth.year
                        sending_dict = {
                            'first_name': emp['name'],
                            'last name': emp['lastname'],
                            'email': f'{emp["name"]}.{emp["lastname"]}@testcompany.com',
                            'age': age,
                            'topic': 'birthday'
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
                            'last_name': emp['lastname'],
                            'email': f'{emp["name"]}.{emp["lastname"]}@testcompany.com',
                            'age': age,
                            'topic': 'birthday'
                        }
                        sending_list.append(sending_dict)

    return sending_list


def send_birthday_email(sending_list):
    """"Send Happy Birthday Messages """
    subject = 'Happy Birthday'
    from_email = settings.EMAIL_HOST_USER
    today = datetime.today()
    birthday_sent_model = BirthdayEmailSent
    sent_query = birthday_sent_model.objects.filter(date=today)
    with open(str(settings.BASE_DIR) + '/templates/happy_birthday.txt') as file:
        birthday_message = file.read()
    for sending in sending_list:
        msg_check = sent_query.filter(recipient=sending['email'])
        to_email = [sending['email']]
        if not msg_check:
            message = EmailMultiAlternatives(subject=subject, body=birthday_message, from_email=from_email, to=to_email)
            html_template = get_template('happy_birthday.html').render(context={'name': sending['first_name']})
            message.attach_alternative(html_template, 'text/html')
            message.send()
            check = birthday_sent_model.objects.create(recipient=sending['email'], date=today, message_sent=True)
            check.save()
        elif msg_check.get(recipient=sending['email']).message_sent == 'False':
            message = EmailMultiAlternatives(subject=subject, body=birthday_message, from_email=from_email, to=to_email)
            html_template = get_template('happy_birthday.html').render(context={'name': sending['first_name']})
            message.attach_alternative(html_template, 'text/html')
            message.send()
            check = msg_check.get(recipient=sending['email'])
            check.message_sent = True
            check.save()

    return 'Birthday Messages Sent'


def happy_birthday():
    """"Function to send birthday messages to all employees if their birthday is today"""
    api_data = employees_api_call()
    exclusions = exclude_api_call()
    birthdays = parse_api_for_exlusions(api_data, exclusions)
    # send_msg = send_birthday_email(birthdays)
    send_message = send_email_message(subject='Happy Birthday', sending_list=birthdays)

    return send_message
