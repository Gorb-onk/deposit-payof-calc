from dataclasses import dataclass
from datetime import date as _date
from decimal import Decimal


@dataclass
class DepositPayoff:
    date: _date
    amount: Decimal
