import unittest
from copy import deepcopy
from billing.calc import compute_invoice

class BillingTests(unittest.TestCase):
    def test_rounding_and_shape(self):
        items = [{"sku": "A", "quantity": 1, "unit_price": "1.005"},
                 {"sku": "B", "quantity": 2, "unit_price": "2.50", "taxable": False}]
        before = deepcopy(items)
        report = compute_invoice(items, tax_rate="0.1", discount_rate="0.1", shipping="0.005")
        self.assertEqual(report["subtotal"], "5.41")
        self.assertEqual(report["tax"], "0.09")
        self.assertEqual(report["total"], "5.51")
        self.assertEqual(report["lines"][0]["gross"], "1.01")
        self.assertEqual(items, before)
    def test_empty(self):
        self.assertEqual(compute_invoice([])["total"], "0.00")
    def test_validation(self):
        with self.assertRaises(ValueError):
            compute_invoice([{"sku": "X", "quantity": True, "unit_price": "1"}])
