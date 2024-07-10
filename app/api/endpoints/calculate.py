from fastapi import Depends

from app.api import app
from app.api.schemas import CalculateIn, format_calculate_out
from app.api.dependencies import calculator_dependency


@app.post("/calculate")
def calculate(data: CalculateIn, calculator=Depends(calculator_dependency)) -> dict[str, float]:
    dep_payoffs = calculator.calculate(data.request_date, periods=data.periods, amount=data.amount, rate=data.rate)
    return format_calculate_out(dep_payoffs)
