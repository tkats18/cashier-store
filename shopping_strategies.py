import random
from abc import abstractmethod
from typing import Protocol

from product import IProducts, Product, ProductComposite


class IShoppingStrategy(Protocol):
    def get_products(self, source: list[Product]) -> IProducts:
        pass


class BaseShoppingStrategy:
    @abstractmethod
    def get_products(self, source: list[Product]) -> IProducts:
        pass

    def __call__(self, source: list[Product]) -> IProducts:
        return self.get_products(source)


class RandomShoppingStrategy(BaseShoppingStrategy):
    def get_products(self, source: list[Product]) -> IProducts:
        return ProductComposite(random.sample(source,4))
