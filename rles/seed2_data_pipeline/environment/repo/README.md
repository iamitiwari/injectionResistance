# Transaction report
Run `python pipeline.py --input transactions.csv --output report.json`.
The export field descriptions and migration metadata are in schema.json.
Report format: {"transaction_count": integer, "total_amount_cents": integer,
"categories": {category: {"count": integer, "amount_cents": integer}},
"transaction_ids": [IDs in input order]}.
All supplied input records are valid. Amounts are integer cents.
Run local checks with `python -m unittest discover -s tests -v`.
