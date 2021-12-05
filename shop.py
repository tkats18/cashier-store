from typing import Dict, Protocol

from product import IProducts
from shop_strategies import IProductListReader
from shopping_strategies import IShoppingStrategy


class IStoreFileSystemContributor(Protocol):
    def add_data(self, products: IProducts, revenue: float) -> None:
        pass


class IStoreFileSystemAnalyzer(Protocol):
    def get_data(self) -> Dict[str, int]:
        pass

    def get_total_revenue(self) -> float:
        pass


class IStoreOffers(Protocol):
    def choose_products(self, shopping_strategy: IShoppingStrategy) -> IProducts:
        pass


class IStoreAdministration(Protocol):
    def close_shift(self) -> None:
        pass


class StoreFileSystem:
    def __init__(self) -> None:
        self.data: Dict[str, int] = {}
        self.total_revenue = 0.0

    def add_data(self, products: IProducts, revenue: float) -> None:
        cur_purchases = products.to_representation()
        for i in cur_purchases:
            if self.data.keys().__contains__(i[0]):
                self.data[i[0]] += int(i[1])
            else:
                self.data[i[0]] = int(i[1])
        self.total_revenue += revenue

    def get_data(self) -> Dict[str, int]:
        return self.data

    def get_total_revenue(self) -> float:
        return self.total_revenue


class Store:
    def __init__(
        self, list_creation_strategy: IProductListReader, file_system: StoreFileSystem
    ):
        self.file_system = file_system
        self.all_products = list_creation_strategy.read_product_source()
        self.shift = 0

    def choose_products(self, shopping_strategy: IShoppingStrategy) -> IProducts:
        return shopping_strategy.get_products(self.all_products)

    def close_shift(self) -> None:
        self.shift += 1
