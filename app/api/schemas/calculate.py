from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

CALC_DATE_FORMAT = '%d.%m.%Y'


class CalculateIn(BaseModel):
    request_date: date = Field(description='Дата заявки', alias='date', examples=['31.01.2021'])
    periods: int = Field(gt=0, lt=61, description='Количество месяцев по вкладу', examples=[1, 3, 60])
    amount: int = Field(gt=9_999, lt=3_000_001, description='Сумма вклада', examples=[10_000, 50_000])
    rate: int = Field(gt=0, lt=9, description='Процент по вкладу', examples=[1, 3, 6])

    @field_validator('request_date', mode='before')
    def string_to_date(cls, date_str: str) -> date:
        return datetime.strptime(date_str, CALC_DATE_FORMAT).date()
