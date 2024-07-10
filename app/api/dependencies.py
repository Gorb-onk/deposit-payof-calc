from app.services.deposit_calculator import DepositCalculator


def calculator_dependency():
    return DepositCalculator()
