from datetime import datetime

import requests


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
    # today = datetime.strptime('2022-10-29', "%Y-%m-%d")
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


def happy_birthday():
    api_data = employees_api_call()
    exclusions = exclude_api_call()
    birthdays = parse_api_for_exlusions(api_data, exclusions)

    return birthdays
