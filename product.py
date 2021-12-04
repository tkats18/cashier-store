from typing import Protocol, List

from dicount import IDiscountData, IDiscountableProduct

"""
ეს არის გარე ინტერფეისი რასაც დაინახავს ის 
"""


class IProducts(Protocol):
    def calculate_total_price(self, discounts: IDiscountData) -> float:
        pass

    def contains(self, discountable: IDiscountableProduct) -> bool:
        pass

    def generate_receipt_line(self, discounts: IDiscountData) -> str:
        pass


# @dataclass(init=True, frozen=True)
class Product(IProducts):
    def __init__(self, name: str, units: int, price: float):
        self.name = name
        self.units = units
        self.price = price

    def calculate_total_price(self, discounts: IDiscountData) -> float:
        return self.price * self.units * discounts.get_discount(self)

    def contains(self, discountable: IDiscountableProduct) -> bool:
        return discountable.get_name() == self.name and discountable.get_units() == self.units

    def generate_receipt_line(self, discounts: IDiscountData) -> str:
        return str(self.units) + self.name + str(self.calculate_total_price(discounts))

    def get_name(self) -> str:
        return self.name

    def get_units(self) -> int:
        return self.units


class ProductComposite(IProducts):
    def __init__(self, products: List[IProducts]):
        self.products = products

    def calculate_total_price(self, discounts: IDiscountData):
        return sum(i.calculate_total_price(discounts) for i in self.products)

    def contains(self, discountable: IDiscountableProduct) -> bool:

        for i in self.products:
            if i.contains(discountable):
                return True

        return False

    # ეს მეთოდი ამას უნდა ქონდეს თუ არა არვიცი მარა თუ არ უნდა ქონდეს
    # მარა თუ არ უნდა ქონდეს receipt_generator ს ან რამეს დავწერდი.
    # სიმარტივისთვის იყოს ესე :დ
    def generate_receipt_line(self, discounts: IDiscountData) -> str:
        res = ""
        for i in self.products:
            res += i.generate_receipt_line(discounts)
        return res
