import unittest
from datetime import date
from date_parser import parse_date

class TimestampRegressionTests(unittest.TestCase):
    def test_z_timestamp(self):
        self.assertEqual(parse_date("2026-10-10T23:30:00Z"), date(2026, 10, 10))
    def test_offset_keeps_local_date(self):
        self.assertEqual(parse_date("2024-02-29T00:01:00.125+14:00"), date(2024, 2, 29))
