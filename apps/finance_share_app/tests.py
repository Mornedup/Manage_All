from django.test import TestCase

# Create your tests here.
from apps.finance_share_app.logic import *


class DaterangeTestCase(TestCase):
    def setUp(self):
        pass

    def test_date_range_1(self):
        dateutil = DateUtils()
        current_date = '2018-11-29'
        current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        daterange = dateutil.get_default_date_range(today=current_date)
        self.assertEqual(daterange['start_date'], datetime.datetime(2018, 11, 26, 0, 0))
        self.assertEqual(daterange['end_date'], datetime.datetime(2018, 12, 26, 0, 0))

    def test_date_range_2(self):
        dateutil = DateUtils()
        current_date = '2018-12-25'
        current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        daterange = dateutil.get_default_date_range(today=current_date)
        self.assertEqual(daterange['start_date'], datetime.datetime(2018, 11, 26, 0, 0))
        self.assertEqual(daterange['end_date'], datetime.datetime(2018, 12, 26, 0, 0))

    def test_date_range_3(self):
        dateutil = DateUtils()
        current_date = '2018-12-28'
        current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        daterange = dateutil.get_default_date_range(today=current_date)
        self.assertEqual(daterange['start_date'], datetime.datetime(2018, 12, 26, 0, 0))
        self.assertEqual(daterange['end_date'], datetime.datetime(2019, 1, 26, 0, 0))

    def test_date_range_4(self):
        dateutil = DateUtils()
        current_date = '2019-01-03'
        current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        daterange = dateutil.get_default_date_range(today=current_date)
        self.assertEqual(daterange['start_date'], datetime.datetime(2018, 12, 26, 0, 0))
        self.assertEqual(daterange['end_date'], datetime.datetime(2019, 1, 26, 0, 0))

    def test_date_range_5(self):
        dateutil = DateUtils()
        months = -3
        current_date = '2018-12-05'
        current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        daterange = dateutil.get_default_date_range(today=current_date, months=months)
        print (daterange)
        self.assertEqual(daterange['start_date'], datetime.datetime(2018, 8, 26, 0, 0))
        self.assertEqual(daterange['end_date'], datetime.datetime(2018, 9, 26, 0, 0))

    def test_date_range_6(self):
        dateutil = DateUtils()
        months = 2
        current_date = '2018-11-23'
        current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        daterange = dateutil.get_default_date_range(today=current_date, months=months)
        self.assertEqual(daterange['start_date'], datetime.datetime(2018, 12, 26, 0, 0))
        self.assertEqual(daterange['end_date'], datetime.datetime(2019, 1, 26, 0, 0))


# class DaterangeTestCase2(TestCase):
#     def setUp(self):
#         pass
#
#     def test_date_range_21(self):
#         dateutil = DateUtils()
#         current_date = '2018-11-29'
#         current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
#         daterange = dateutil.get_range(input_date=current_date, day_offset=25)
#         print("day: ", current_date, "/n start: ", daterange['start_date'], "/n end: ", daterange['end_date'])
#         self.assertEqual(daterange['start_date'], datetime.datetime(2018, 11, 26, 0, 0))
#         self.assertEqual(daterange['end_date'], datetime.datetime(2018, 12, 26, 0, 0))
#
#     def test_date_range_22(self):
#         dateutil = DateUtils()
#         current_date = '2018-12-25'
#         current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
#         daterange = dateutil.get_range(input_date=current_date, day_offset=25)
#         self.assertEqual(daterange['start_date'], datetime.datetime(2018, 11, 26, 0, 0))
#         self.assertEqual(daterange['end_date'], datetime.datetime(2018, 12, 26, 0, 0))
#
#     def test_date_range_23(self):
#         dateutil = DateUtils()
#         current_date = '2018-12-28'
#         current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
#         daterange = dateutil.get_range(input_date=current_date, day_offset=25)
#         self.assertEqual(daterange['start_date'], datetime.datetime(2018, 12, 26, 0, 0))
#         self.assertEqual(daterange['end_date'], datetime.datetime(2019, 1, 26, 0, 0))
#
#     def test_date_range_24(self):
#         dateutil = DateUtils()
#         current_date = '2019-01-03'
#         current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
#         daterange = dateutil.get_range(input_date=current_date, day_offset=25)
#         self.assertEqual(daterange['start_date'], datetime.datetime(2018, 12, 26, 0, 0))
#         self.assertEqual(daterange['end_date'], datetime.datetime(2019, 1, 26, 0, 0))
