from dateutil.relativedelta import relativedelta

from app.api import app
from app.api.schemas import CalculateIn, CALC_DATE_FORMAT


@app.get("/calculate")
def process_transaction(data: CalculateIn) -> dict[str, int]:
    result = {}
    for i in range(data.periods):
        date = data.request_date + relativedelta(months=i)
        result[date.strftime(CALC_DATE_FORMAT)] = i
    return result
