from typing import List, Optional, Protocol, Tuple

from dicount import DiscountableProduct, IDiscountableProduct, IDiscountData


# ეს არის გარე ინტერფეისი რასაც დაინახავს ის
class IProducts(Protocol):
    def calculate_total_price(self, discounts: Optional[IDiscountData]) -> float:
        pass

    def contains(self, discountable: IDiscountableProduct) -> bool:
        pass

    def to_full_representation(
        self, discounts: Optional[IDiscountData]
    ) -> List[Tuple[str, str, str, str]]:
        pass

    def to_representation(self) -> List[Tuple[str, str]]:
        pass


class Product:
    def __init__(self, name: str, units: int, price: float):
        self.name = name
        self.units = units
        self.price = price

    def calculate_total_price(self, discounts: Optional[IDiscountData]) -> float:
        price_not_filled = self.price * self.units
        if discounts is None:
            return price_not_filled

        price_not_filled *= 1 - discounts.get_discount(
            DiscountableProduct(self.name, self.units)
        )
        return (1 - discounts.get_total_discount()) * price_not_filled

    def contains(self, discountable: IDiscountableProduct) -> bool:
        return (
            discountable.get_name() == self.name
            and discountable.get_units() == self.units
        )

    def to_full_representation(
        self, discounts: Optional[IDiscountData]
    ) -> List[Tuple[str, str, str, str]]:
        return [
            (
                self.name,
                str(self.units),
                str(self.price),
                str(self.calculate_total_price(discounts)),
            )
        ]

    def to_representation(self) -> List[Tuple[str, str]]:
        return [(self.name, str(self.units))]


class ProductComposite:
    def __init__(self, products: List[IProducts]):
        self.products = products

    def calculate_total_price(self, discounts: Optional[IDiscountData]) -> float:
        return sum(i.calculate_total_price(discounts) for i in self.products)

    def contains(self, discountable: IDiscountableProduct) -> bool:

        for i in self.products:
            if i.contains(discountable):
                return True

        return False

    # ეს მეთოდი ამას უნდა ქონდეს თუ არა არვიცი მარა თუ არ უნდა ქონდეს
    # მარა თუ არ უნდა ქონდეს receipt_generator ს ან რამეს დავწერდი.
    # სიმარტივისთვის იყოს ესე :დ
    def to_full_representation(
        self, discounts: Optional[IDiscountData]
    ) -> List[Tuple[str, str, str, str]]:
        return list(
            map(lambda x: x.to_full_representation(discounts)[0], self.products)
        )

    def to_representation(self) -> List[Tuple[str, str]]:
        return list(map(lambda x: x.to_representation()[0], self.products))
