from dataclasses import dataclass
from typing import Protocol

from discount_manager import IDiscountCalculator
from product import IProducts
from receipt import Receipt
from shop import IStoreFileSystemContributor


class IReceiptOpener(Protocol):
    def open_receipt(self) -> Receipt:
        pass


class IReceiptFiller(Protocol):
    def fill_items_to_receipt(self, receipt: Receipt, products: IProducts) -> Receipt:
        pass


class IPaymentConfirm(Protocol):
    def confirm_payment(self, receipt: Receipt, paid_amount: float):
        pass


@dataclass
class Cashier:
    discount_calculator: IDiscountCalculator
    store_file_system: IStoreFileSystemContributor

    def open_receipt(self) -> Receipt:
        return Receipt(False, None, None)

    def fill_items_to_receipt(self, receipt: Receipt, products: IProducts) -> Receipt:
        receipt.products = products
        receipt.discounts = self.discount_calculator.calculate_discounts(products)
        print(receipt.get_receipt_string())
        return receipt

    def confirm_payment(self, receipt: Receipt, paid_amount: float):
        if receipt.get_total_price() <= paid_amount:
            self.store_file_system.add_data(receipt.products, receipt.get_total_price())
        else:
            print("CASHIER--- msg: not enough amount")
