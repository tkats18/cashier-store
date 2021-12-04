from dataclasses import dataclass
from typing import Optional

from dicount import IDiscountData
from product import IProducts


@dataclass
class Receipt:
    paid: bool
    products: Optional[IProducts]
    discounts: Optional[IDiscountData]

    def get_total_price(self) -> float:
        return self.products.calculate_total_price(self.discounts)

    def get_receipt_string(self) -> str:
        return self.products.generate_receipt_line(self.discounts)
