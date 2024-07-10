from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.dto import DepositPayoff

CALC_DATE_FORMAT = '%d.%m.%Y'


class CalculateIn(BaseModel):
    request_date: date = Field(description='Дата заявки', alias='date', examples=['31.01.2021'])
    periods: int = Field(gt=0, lt=61, description='Количество месяцев по вкладу', examples=[1, 3, 60])
    amount: int = Field(gt=9_999, lt=3_000_001, description='Сумма вклада', examples=[10_000, 50_000])
    rate: int = Field(gt=0, lt=9, description='Процент по вкладу', examples=[1, 3, 6])

    @field_validator('request_date', mode='before')
    def string_to_date(cls, raw_date: Any) -> date:
        if isinstance(raw_date, str):
            return datetime.strptime(raw_date, CALC_DATE_FORMAT).date()
        else:
            return raw_date


def format_calculate_out(payoffs: list[DepositPayoff]) -> dict:
    result = {}
    for payoff in sorted(payoffs, key=lambda x: x.date):
        date_str = payoff.date.strftime(CALC_DATE_FORMAT)
        result[date_str] = "{:.2f}".format(payoff.amount)
    return result
