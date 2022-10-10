from django.test import TestCase

from msg.utils import employees_api_call, exclude_api_call, happy_birthday, check_leap_year


# Create your tests here.
class BirthdayTests(TestCase):

    def test_employees_api_call(self):
        call = employees_api_call().status_code
        self.assertEqual(call, 200)

    def test_exclude_api_call(self):
        call = exclude_api_call()
        self.assertEqual(call, [223, 239, 313])

    def test_happy_birthday(self):
        happy = happy_birthday()
        self.assertEqual(happy, 'Emails have been sent')

    def test_check_leap_year(self):
        leap = check_leap_year(2020)
        not_leap = check_leap_year(2022)
        self.assertTrue(leap)
        self.assertFalse(not_leap)
