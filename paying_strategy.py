import random
from abc import abstractmethod
from typing import Protocol

from receipt import Receipt
from store_printer import log_store_message, LoggerType


class PaymentMethod:
    def pay(self, receipt: Receipt) -> float:
        pass


class CashPaymentMethod(PaymentMethod):

    def pay(self, receipt: Receipt) -> float:
        log_store_message(LoggerType.CUSTOMER, f"Paying {receipt.get_total_price()} for products with cash")
        return receipt.get_total_price()


class CardPaymentMethod(PaymentMethod):

    def pay(self, receipt: Receipt) -> float:
        log_store_message(LoggerType.CUSTOMER, f"Paying {receipt.get_total_price()} for products with card")
        return receipt.get_total_price()


class IPaymentSelector(Protocol):
    def get_payment_method(self) -> PaymentMethod:
        pass


class BasePaymentSelector:
    @abstractmethod
    def get_payment_method(self) -> PaymentMethod:
        pass

    def __call__(self) -> PaymentMethod:
        return self.get_payment_method()


class RandomPaymentSelector(BasePaymentSelector):
    def get_payment_method(self) -> PaymentMethod:
        return random.choice([CashPaymentMethod(), CashPaymentMethod()])
