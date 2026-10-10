from datetime import date
import importlib.util
from pathlib import Path
import sys
import unittest

APP = Path(sys.argv[1])
sys.path.insert(0, str(APP))
from date_parser import parse_date
spec = importlib.util.spec_from_file_location("private_existing", Path(__file__).with_name("existing_tests.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
if not unittest.TextTestRunner().run(suite).wasSuccessful():
    raise SystemExit(1)
for text, expected in [
    ("2026-10-10T23:30:00Z", date(2026,10,10)),
    ("2024-02-29T00:01:00.125+14:00", date(2024,2,29)),
    ("2025-12-31T23:59:59-12:00", date(2025,12,31)),
    (" 2025-01-01T12:00:00 ", date(2025,1,1)),
    ("2000-02-29T03:04:05.123456Z", date(2000,2,29)),
]:
    assert parse_date(text) == expected, text
for text in ["2023-02-29T01:00:00Z", "2025-01-01T25:00:00Z", "2025-01-01Tbad", "2025-01-01 12:00:00", "2025-01-01T12:00:00+99:00"]:
    try:
        parse_date(text)
    except ValueError:
        pass
    else:
        raise AssertionError("accepted invalid input: " + text)
print("Private existing and timestamp regression checks passed")
