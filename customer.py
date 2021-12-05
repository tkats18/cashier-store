from dataclasses import dataclass
from typing import Protocol

from paying_strategy import IPaymentSelector
from product import IProducts
from receipt import Receipt
from shop import IStoreOffers
from shopping_strategies import IShoppingStrategy


class IProductChooser(Protocol):

    def choose_products(self) -> IProducts:
        pass


class IPayer(Protocol):
    def pay(self, receipt: Receipt) -> float:
        pass


@dataclass
class Customer:
    store_offers: IStoreOffers
    shopping_strategy: IShoppingStrategy
    payment: IPaymentSelector

    def choose_products(self) -> IProducts:
        return self.store_offers.choose_products(self.shopping_strategy)

    def pay(self, receipt: Receipt) -> float:
        method = self.payment.get_payment_method()
        return method.pay(receipt=receipt)
