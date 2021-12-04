from typing import Protocol

from customer_strategies import IShoppingStrategy
from product import IProducts
from shop_strategies import IProductListReader


class IStoreFileSystem(Protocol):
    def add_data(self, products: IProducts, revenue: float):
        pass


class IStoreOffers(Protocol):
    def choose_products(self, shopping_strategy: IShoppingStrategy) -> IProducts:
        pass





class StoreFileSystem:

    def add_data(self, products: IProducts, revenue: float):
        # todo
        pass


class Store:

    def __init__(self, list_creation_strategy: IProductListReader):
        self.file_system = StoreFileSystem()
        self.all_products = list_creation_strategy.read_product_source()

    def choose_products(self, shopping_strategy: IShoppingStrategy) -> IProducts:
        return shopping_strategy.get_products(self.all_products)
