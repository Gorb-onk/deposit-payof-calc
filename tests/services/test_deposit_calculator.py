from datetime import date
from decimal import Decimal

import pytest
from dateutil.relativedelta import relativedelta

from app.services.deposit_calculator import DepositCalculator


@pytest.mark.parametrize("amount, rate, result", (
        (10000, 10, Decimal('10083.33333333333333333333333')),
        (1000, 12, Decimal('1010'))
))
def test_default_formula(amount, rate, result):
    assert DepositCalculator.default_formula(amount, rate) == result


@pytest.mark.parametrize("amount, rate, result", (
        (10000, 10, Decimal('10010')),
        (1000, 12, Decimal('1012'))
))
def test_custom_formula(amount, rate, result):
    calculator = DepositCalculator(lambda x, y: x + y)
    assert calculator.formula(amount, rate) == result


@pytest.mark.parametrize("date_, amount, rate, periods",
                         ((date(year=2021, month=1, day=1), 1000, 10, 10),
                          (date(year=2021, month=1, day=1), 59_349, 12, 53),
                          (date(year=2021, month=1, day=1), 500_000, 7, 44)))
def test_calculation(date_, amount, rate, periods):
    calculator = DepositCalculator(lambda x, y: x + y)

    result = calculator.calculate(date_, periods, amount, rate)

    assert len(result) == periods
    for i, deposit_payoff in enumerate(result):
        assert deposit_payoff.date - relativedelta(months=i) == date_
        assert deposit_payoff.amount == amount + rate * (i + 1)
