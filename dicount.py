from dataclasses import dataclass
from typing import Dict, Protocol, List, Optional, Any

"""
ამ კლასს ვაკეთებ იმიტო რომ მომავალში ვთქვათ ველი რომ
დაემატოს პროდუქტს იმპურტულია თუ არადა მაგის მიხედვით
რომ იყო ფასდაკლება ან რამე უბალოდ აქ დავამატებთ 
get_is_imported მეთოდს და productis ქომფეარში ერთ and ს
ჩავამატებთ (ანუ არ გვალიძულებს რომ მაინცდამაინც სახელით 
და იუნიტების მიხედვით იყოს დიქაუნით)
"""


class IDiscountableProduct(Protocol):

    def get_name(self) -> str:
        pass

    def get_units(self) -> int:
        pass


class DiscountableProduct(IDiscountableProduct):
    def __init__(self, name: str, units: int):
        self.name = name
        self.units = units

    def get_units(self) -> int:
        return self.units

    def get_name(self) -> str:
        return self.name


# ეს მარტო იმიტო დამჭირდა რომ მეპში რახან ლისტს ვინახავ
# როგორც ქის ლისტი ჰეშირებადი არაა
class IDiscountableProductList:

    def get_list(self) -> List[IDiscountableProduct]:
        pass


class DiscountableProductList(IDiscountableProductList):
    def __init__(self, discountable_prod_list: List[IDiscountableProduct]):
        self.discountable_prod_list = discountable_prod_list

    def get_list(self) -> List[IDiscountableProduct]:
        return self.discountable_prod_list


# კონკრეტული ვაჭრობის დისქაუნთის კონფიგურაცია
# გააჩნია იმის განმსაზღვრელი თუ რამდენი არის მთლიანი ფასის
# დისქაუნთი და ასევე გააჩნია მეპის გეთერ მეთოდი get_discount
# რომელიც იმას განსაზღვრავს კონკრეტულ პროდუქტზე ცალკე დისქაუნთი თუ მოქმედებს.
class IDiscountData(Protocol):
    def get_discount(self, product: IDiscountableProduct) -> float:
        pass

    def get_total_discount(self) -> float:
        pass


@dataclass
class DiscountData:
    discount_by_product: Dict[IDiscountableProduct, float]
    total_discount: float

    def get_discount(self, product: IDiscountableProduct) -> float:
        if not self.discount_by_product.keys().__contains__(product):
            return 1.0
        else:
            return self.discount_by_product[product]

    def get_total_discount(self) -> float:
        return self.total_discount


class IDiscountDataBuilder(Protocol):
    def with_discount(self, product: IDiscountableProduct, value: float) -> "IDiscountDataBuilder":
        pass

    def with_total_discount(self, *, total_amount: int) -> "IDiscountDataBuilder":
        pass

    def build(self) -> IDiscountData:
        pass


class DiscountDataBuilder:
    def __init__(self, kwargs: Optional[Dict[Any, Any]] = None):
        self.kwargs = kwargs or {}

    def with_discount(self, product: IDiscountableProduct, value: float) -> "DiscountDataBuilder":
        self.kwargs.setdefault("discounts", {})
        self.kwargs["discounts"][product] = value
        return self

    def with_total_discount(self, *, total_amount: float) -> "DiscountDataBuilder":
        self.kwargs.setdefault("total_amount", total_amount)
        return self

    def build(self) -> IDiscountData:
        return DiscountData(self.kwargs['discounts'] if self.kwargs.keys().__contains__('discounts') else dict(),
                            self.kwargs['total_amount'] if self.kwargs.keys().__contains__('total_amount') else 1.0)
