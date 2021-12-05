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
        total = 0
        res = "\n" + '{:10s} {:1s} {:5s} {:1s} {:5s} {:1s} {:5s} {:1s}'.format("Name", "|", "Units", "|", "Price", "|",
                                                                               "Total", "|") + "\n"
        res += '{:10s} {:1s} {:5s} {:1s} {:5s} {:1s} {:5s} {:1s}'.format("----------", "|", "-----", "|",
                                                                         "-----", "|", "-----", "|")

        data = self.products.to_full_representation(self.discounts)
        for i in data:
            res += "\n" + '{:10s} {:1s} {:5s} {:1s} {:5s} {:1s} {:5s} {:1s}'.format(i[0], "|", i[1], "|", i[2],
                                                                                    "|", i[3], "|")
            total += float(i[3])
        res += "\nSum: " + str(total) + "\n"
        return res
