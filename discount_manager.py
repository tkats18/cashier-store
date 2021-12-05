from typing import Optional, Protocol

from dicount import DiscountDataBuilder, IDiscountData
from discount_strategies import IDiscountDataAcquiringStrategy
from product import IProducts


class IDiscountCalculator(Protocol):
    def calculate_discounts(self, products: Optional[IProducts]) -> IDiscountData:
        pass


class DiscountManager:
    def __init__(self, strategy: IDiscountDataAcquiringStrategy):
        self.discount_data = strategy.get_discount_data()

    def calculate_discounts(self, products: Optional[IProducts]) -> IDiscountData:
        total = 0.0
        discount_data_builder = DiscountDataBuilder()

        if products is None:
            return discount_data_builder.build()

        for i in self.discount_data:
            contains_all = True
            for j in i.get_list():
                if not products.contains(j):
                    contains_all = False
                    break
            if contains_all:
                for k in i.get_list():
                    discount_data_builder.with_discount(
                        k, self.discount_data[i].get_discount(k)
                    )

                total += self.discount_data[i].get_total_discount()

        return discount_data_builder.with_total_discount(total_amount=total).build()
