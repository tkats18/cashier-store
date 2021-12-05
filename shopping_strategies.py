import random
from abc import abstractmethod
from typing import List, Protocol

from product import IProducts, Product, ProductComposite


class IShoppingStrategy(Protocol):
    def get_products(self, source: List[Product]) -> IProducts:
        pass


class BaseShoppingStrategy:
    @abstractmethod
    def get_products(self, source: List[Product]) -> IProducts:
        pass

    def __call__(self, source: List[Product]) -> IProducts:
        return self.get_products(source)


class RandomShoppingStrategy(BaseShoppingStrategy):
    def get_products(self, source: List[Product]) -> IProducts:
        return ProductComposite(random.sample(source, 4))


class FixedShoppingStrategy(BaseShoppingStrategy):
    def get_products(self, source: List[Product]) -> IProducts:
        return source[0]


class DoubleFixedShoppingStrategy(BaseShoppingStrategy):
    def get_products(self, source: List[Product]) -> IProducts:
        return ProductComposite([source[0], source[8]])


class CustomFixedShoppingStrategy(BaseShoppingStrategy):
    def get_products(self, source: List[Product]) -> IProducts:
        return ProductComposite([source[4], source[2]])
