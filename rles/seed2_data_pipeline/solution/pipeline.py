import csv


def read_transactions(path):
    with open(path, newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


import argparse
import json
from pathlib import Path


def summarize(rows):
    report = {"transaction_count": 0, "total_amount_cents": 0, "categories": {}, "transaction_ids": []}
    for row in rows:
        amount = int(row["amount_cents"])
        category = report["categories"].setdefault(row["category"], {"count": 0, "amount_cents": 0})
        category["count"] += 1
        category["amount_cents"] += amount
        report["transaction_count"] += 1
        report["total_amount_cents"] += amount
        report["transaction_ids"].append(row["transaction_id"])
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    Path(args.output).write_text(json.dumps(summarize(read_transactions(args.input)), indent=2) + "\n")


if __name__ == "__main__":
    main()
