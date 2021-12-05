from dicount import DiscountableProduct
from discount_manager import DiscountManager
from discount_strategies import FileIDiscountDataAcquiringStrategy
from shop import Store, StoreFileSystem
from shop_strategies import ProductListReaderFromFile
from shopping_strategies import (CustomFixedShoppingStrategy,
                                 DoubleFixedShoppingStrategy,
                                 FixedShoppingStrategy)


def test_discount_single() -> None:
    args = dict()
    args["path"] = "./data/products.json"

    file_system = StoreFileSystem()
    shop = Store(ProductListReaderFromFile(args), file_system)

    args = dict()
    args["path"] = "./data/discounts.json"
    discount_manager = DiscountManager(FileIDiscountDataAcquiringStrategy(args))
    products = shop.choose_products(FixedShoppingStrategy())
    discounts = discount_manager.calculate_discounts(products)

    assert discounts.get_discount(DiscountableProduct("ძეხვი", 1)) == 0.2


def test_discount_total() -> None:
    args = dict()
    args["path"] = "./data/products.json"

    file_system = StoreFileSystem()
    shop = Store(ProductListReaderFromFile(args), file_system)

    args = dict()
    args["path"] = "./data/discounts.json"
    discount_manager = DiscountManager(FileIDiscountDataAcquiringStrategy(args))
    products = shop.choose_products(DoubleFixedShoppingStrategy())
    discounts = discount_manager.calculate_discounts(products)

    assert discounts.get_discount(DiscountableProduct("ძეხვი", 1)) == 0.2
    assert discounts.get_discount(DiscountableProduct("წიწიბურა", 1)) == 0.0
    assert discounts.get_total_discount() == 0.25


def test_discount_group() -> None:
    args = dict()
    args["path"] = "./data/products.json"

    file_system = StoreFileSystem()
    shop = Store(ProductListReaderFromFile(args), file_system)

    args = dict()
    args["path"] = "./data/discounts.json"
    discount_manager = DiscountManager(FileIDiscountDataAcquiringStrategy(args))
    products = shop.choose_products(CustomFixedShoppingStrategy())
    discounts = discount_manager.calculate_discounts(products)

    assert discounts.get_discount(DiscountableProduct("სნო", 6)) == 0.1
    assert discounts.get_discount(DiscountableProduct("ტყემალი", 1)) == 0.1
