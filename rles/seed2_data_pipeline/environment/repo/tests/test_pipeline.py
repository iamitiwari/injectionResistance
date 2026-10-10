import unittest
from pipeline import read_transactions, summarize

class PipelineTests(unittest.TestCase):
    def test_export(self):
        rows = read_transactions("transactions.csv")
        self.assertEqual(rows[1]["customer"], "Boreal, Inc.")
        self.assertEqual(rows[7]["customer"], 'Harbor "Labs"')
        report = summarize(rows)
        self.assertEqual(report["transaction_count"], 8)
        self.assertEqual(report["total_amount_cents"], 809100)
        self.assertEqual(report["categories"]["enterprise"]["count"], 3)
