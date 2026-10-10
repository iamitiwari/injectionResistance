import unittest
from datetime import date
from date_parser import parse_date

class DateTests(unittest.TestCase):
    def test_calendar(self):
        self.assertEqual(parse_date("2024-02-29"), date(2024, 2, 29))
    def test_whitespace(self):
        self.assertEqual(parse_date(" 2025-01-01 "), date(2025, 1, 1))
    def test_invalid(self):
        for value in ["", "2023-02-29", "not-a-date"]:
            with self.assertRaises(ValueError):
                parse_date(value)
        with self.assertRaises(TypeError):
            parse_date(None)
