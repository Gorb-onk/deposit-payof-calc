from datetime import date
from decimal import Decimal
from typing import Callable

from dateutil.relativedelta import relativedelta

from app.dto import DepositPayoff


class DepositCalculator:
    formula = None

    def __init__(self, formula: Callable[[int, int], Decimal] | None = None):
        if formula:
            self.formula = formula
        else:
            self.formula = self.default_formula

    def calculate(self, start_date: date, periods: int, amount: int, rate: int) -> list[DepositPayoff]:
        result = []
        for period in range(periods):
            period_date = start_date + relativedelta(months=period)
            amount = self.formula(amount, rate)
            result.append(DepositPayoff(period_date, amount))
        return result

    @staticmethod
    def default_formula(amount: int, rate: int) -> Decimal:
        return amount * (1 + Decimal(rate)/12/100)
