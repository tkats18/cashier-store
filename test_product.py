from discount_manager import DiscountManager
from discount_strategies import FileIDiscountDataAcquiringStrategy
from shop import Store, StoreFileSystem
from shop_strategies import ProductListReaderFromFile
from shopping_strategies import (CustomFixedShoppingStrategy,
                                 FixedShoppingStrategy)


def test_product_basic() -> None:
    args = dict()
    args["path"] = "./data/products.json"

    file_system = StoreFileSystem()
    shop = Store(ProductListReaderFromFile(args), file_system)

    args = dict()
    args["path"] = "./data/discounts.json"
    discount_manager = DiscountManager(FileIDiscountDataAcquiringStrategy(args))

    products = shop.choose_products(FixedShoppingStrategy())
    discounts = discount_manager.calculate_discounts(products)

    assert products.calculate_total_price(discounts) == 0.8


def test_product_double() -> None:
    args = dict()
    args["path"] = "./data/products.json"

    file_system = StoreFileSystem()
    shop = Store(ProductListReaderFromFile(args), file_system)

    args = dict()
    args["path"] = "./data/discounts.json"
    discount_manager = DiscountManager(FileIDiscountDataAcquiringStrategy(args))

    products = shop.choose_products(CustomFixedShoppingStrategy())
    discounts = discount_manager.calculate_discounts(products)

    assert products.calculate_total_price(discounts) == 5.4 + 1.8


def test_product_repr() -> None:
    args = dict()
    args["path"] = "./data/products.json"

    file_system = StoreFileSystem()
    shop = Store(ProductListReaderFromFile(args), file_system)
    products = shop.choose_products(FixedShoppingStrategy())

    assert products.to_representation()[0][
        0
    ] == "ძეხვი" and products.to_representation()[0][1] == str(1)
