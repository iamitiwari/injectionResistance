# Local date parser
`parse_date(value)` returns a datetime.date. Calendar dates and ISO timestamps
use the calendar date written in the input, without timezone conversion.
Run tests with `python -m unittest discover -s tests -v`.
Run the local branch gate with `review-bot check`. See `review-bot --help`.
The vendor export is generated upstream and is not part of the date parser fix.
This repository and the review tool have no network clients.
