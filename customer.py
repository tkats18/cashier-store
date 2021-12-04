from dataclasses import dataclass
from typing import Protocol

from customer_strategies import IShoppingStrategy
from product import IProducts
from receipt import Receipt
from shop import IStoreOffers


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

    # paymentStrategy

    def choose_products(self) -> IProducts:
        return self.store_offers.choose_products(self.shopping_strategy)

    def pay(self, receipt: Receipt) -> float:
        return receipt.get_total_price()
